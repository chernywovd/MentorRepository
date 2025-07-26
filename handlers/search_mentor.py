from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto

import asyncio

from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from Database import import_mentors
from keyboards import keyboard as kb

from AdminPanel.Admins import admins
from Database.import_mentors import select_mentors_from_db, current_mentors_data
from Sub.Subjects import dict_directions

from Database.Database import DatabaseClass

bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()


directions = list(dict_directions.keys()) # все направления


@router.message(F.text.in_(directions))
async def search_tutor(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние

    current_mentors_data = import_mentors.current_mentors_data
    if current_mentors_data is not None:
        direction = dict_directions[message.text] # направление
        # dict_mentors_sort = (await select_mentors_from_db())["Отсортированные наставники по направлениям"]
        dict_mentors_sort = current_mentors_data["Отсортированные наставники по направлениям"]

        try:
            mentors = dict_mentors_sort[direction]

            list_mentors = ''
            star = ''
            for mentor in mentors:
                mentor_name,  description, price = mentor['Name'], mentor['Description'], mentor['Price']
                if mentor['CallOrder'] == 1:
                    list_mentors += f"<b>{mentor_name}</b>🌟 - {price}\n\n"
                else:
                    list_mentors += f"<b>{mentor_name}</b> - {price}\n\n"

            await bot.send_message(message.from_user.id, f"{list_mentors}",
                                   disable_web_page_preview=True)

        except Exception as ex:
            await bot.send_message(message.from_user.id, f"<b>Проводится набор на должность❗️</b>\n"
                                                         f"На данный момент наставников по этому направлению нет",
                                   disable_web_page_preview=True)
            print(f"Нет наставников на направление {message.text}")
            print(ex)

    else:
        await bot.send_message(message.from_user.id, f"База менторов выгружается\n"
                                                     f"Это займет некоторое время⏳",
                               disable_web_page_preview=True)


@router.message((F.text)[0]=='/')
async def scss(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние

    current_mentors_data = import_mentors.current_mentors_data
    if current_mentors_data is not None:
        try:
            # dict_mentors = (await select_mentors_from_db())["Информация о менторах из базы"]
            dict_mentors = current_mentors_data["Информация о менторах из базы"]
            mentor = next((item for item in dict_mentors if item['Name'] == f"{message.text}"), None)

            mentor_photo = mentor['Photo']
            mentor_id_tg_user_id = mentor['IdTgUserId']
            mentor_id = mentor['Id']
            mentor_name = mentor['OfficialName']
            description = mentor['Description']
            price = mentor['Price']
            detailed_information = mentor['DetailedInformation']
            call_order = mentor['CallOrder']

            star = ''
            if call_order == 1:
                star = '🌟'

            bell = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Забронировать', callback_data=f"Забронировать {mentor_id}")],
                [InlineKeyboardButton(text='Закрыть', callback_data='Закрыть')],
                [InlineKeyboardButton(text='<<', callback_data=f"<<{mentor_id}"), InlineKeyboardButton(text='>>', callback_data=f"{mentor_id}>>")]
                    ])
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=mentor_photo,
                                 caption=f"<b>{mentor_name}</b>{star}\n\n"
                                         f"{description}\n"
                                         f"<a href='{detailed_information}'>подробнее..</a>\n\n"
                                         f"Стоимость: {price}",
                                 reply_markup=bell)
        except Exception as ex:
            print('Пользователь попытался ввести что-то другое через знак «/»')
    else:
        await bot.send_message(message.from_user.id, f"База менторов выгружается\n"
                                                     f"Это займет некоторое время⏳",
                               disable_web_page_preview=True)


@router.callback_query( ((F.data)[0:2] == '<<') |  ((F.data)[-2:] == '>>') )
async def close(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики

    current_mentors_data = import_mentors.current_mentors_data
    if current_mentors_data is not None:
        if (callback.data)[0:2] == '<<':
            id_mentor = int((callback.data)[2:])

            # dict_mentors_sort = (await select_mentors_from_db())["Отсортированные наставники по направлениям"]
            # dict_mentors = (await select_mentors_from_db())["Информация о менторах из базы"]
            dict_mentors_sort = current_mentors_data["Отсортированные наставники по направлениям"]
            dict_mentors = current_mentors_data["Информация о менторах из базы"]

            mentor = next((item for item in dict_mentors if item['Id'] == id_mentor), None)
            subject = mentor["Subject"] #вытаскиваем направление

            list_mentor = dict_mentors_sort[subject] # Вытаскиваем всех активных менторов по этому направлению

            if len(list_mentor) == 1:
                pass
            else:
                for index, mentor_inf in enumerate(list_mentor): #находим нынешнего ментора и выводим на экран следующего за ним в очереди, если нынешний является последним в списке, то выводим на экран первого
                    if mentor_inf.get('Id') == id_mentor:
                        try:
                            mentor = list_mentor[index-1]
                        except:
                            mentor = list_mentor[-1]

                        mentor_photo = mentor['Photo']
                        mentor_id = mentor['Id']
                        mentor_name = mentor['OfficialName']
                        description = mentor['Description']
                        price = mentor['Price']
                        detailed_information = mentor['DetailedInformation']
                        call_order = mentor['CallOrder']

                        star = ''
                        if call_order == 1:
                            star = '🌟'

                        bell = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Забронировать', callback_data=f"Забронировать {mentor_id}")],
                            [InlineKeyboardButton(text='Закрыть', callback_data='Закрыть')],
                            [InlineKeyboardButton(text='<<', callback_data=f"<<{mentor_id}"),
                             InlineKeyboardButton(text='>>', callback_data=f"{mentor_id}>>")]
                        ])

                        await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaPhoto(
                                media=mentor_photo,
                                caption=f"<b>{mentor_name}</b>{star}\n\n"
                                                     f"{description}\n"
                                                     f"<a href='{detailed_information}'>подробнее..</a>\n\n"
                                                     f"Стоимость: {price}"),
                            reply_markup=bell
                        )
                        break


        elif (callback.data)[-2:] == '>>':
            id_mentor = int((callback.data)[:-2])

            # dict_mentors_sort = (await select_mentors_from_db())["Отсортированные наставники по направлениям"]
            # dict_mentors = (await select_mentors_from_db())["Информация о менторах из базы"]
            dict_mentors_sort = current_mentors_data["Отсортированные наставники по направлениям"]
            dict_mentors = current_mentors_data["Информация о менторах из базы"]

            mentor = next((item for item in dict_mentors if item['Id'] == id_mentor), None)
            subject = mentor["Subject"]  # вытаскиваем направление

            list_mentor = dict_mentors_sort[subject]  # Вытаскиваем всех активных менторов по этому направлению

            if len(list_mentor) == 1:
                pass
            else:
                for index, mentor_inf in enumerate(list_mentor): #находим нынешнего ментора и выводим на экран следующего за ним в очереде, если нынешний является последним в списке, то выводим на экран первого
                    if mentor_inf.get('Id') == id_mentor:
                        try:
                            mentor = list_mentor[index+1]
                        except:
                            mentor = list_mentor[0]

                        mentor_photo = mentor['Photo']
                        mentor_id = mentor['Id']
                        mentor_name = mentor['OfficialName']
                        description = mentor['Description']
                        price = mentor['Price']
                        detailed_information = mentor['DetailedInformation']
                        call_order = mentor['CallOrder']

                        star = ''
                        if call_order == 1:
                            star = '🌟'

                        bell = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Забронировать', callback_data=f"Забронировать {mentor_id}")],
                            [InlineKeyboardButton(text='Закрыть', callback_data='Закрыть')],
                            [InlineKeyboardButton(text='<<', callback_data=f"<<{mentor_id}"),
                             InlineKeyboardButton(text='>>', callback_data=f"{mentor_id}>>")]
                        ])

                        await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaPhoto(
                                media=mentor_photo,
                                caption=f"<b>{mentor_name}</b>{star}\n\n"
                                                     f"{description}\n"
                                                     f"<a href='{detailed_information}'>подробнее..</a>\n\n"
                                                     f"Стоимость: {price}"),
                            reply_markup=bell
                        )
                        break
    else:
        await bot.send_message(callback.from_user.id, f"База менторов выгружается\n"
                                                     f"Это займет некоторое время⏳",
                               disable_web_page_preview=True)

@router.callback_query(F.data.in_(['Закрыть', 'Нет, не бронирую']))
async def close(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

@router.callback_query((F.data)[0:13] == f"Забронировать")
async def book(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние

    current_mentors_data = import_mentors.current_mentors_data
    if current_mentors_data is not None:
        mentor_id = int(callback.data[14:]) #id выбранного ментора

        # dict_mentors = (await select_mentors_from_db())["Информация о менторах из базы"]
        dict_mentors = current_mentors_data["Информация о менторах из базы"]
        mentor = next((item for item in dict_mentors if item['Id'] == mentor_id), None)

        mentor_photo = mentor['Photo']

        yes_or_no = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data=f"Да, бронирую {mentor_id}"),
             InlineKeyboardButton(text='Нет', callback_data='Нет, не бронирую')]
                ])

        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=mentor_photo,
                caption=f"Подтвердите запись на встречу с ментором"),
            reply_markup=yes_or_no
        )
    else:
        await bot.send_message(callback.from_user.id, f"Ощибка! База менторов ещё выгружается\n"
                                                      f"Это займет некоторое время⏳",
                               disable_web_page_preview=True)

@router.callback_query((F.data)[0:12] == f"Да, бронирую")
async def book(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    current_mentors_data = import_mentors.current_mentors_data
    if current_mentors_data is not None:
        work_database = DatabaseClass(TgUserID=callback.from_user.id)

        mentor_id_tg_user_id = int(callback.data[13:]) #id выбранного ментора

        # dict_mentors = (await select_mentors_from_db())["Информация о менторах из базы"]
        dict_mentors = current_mentors_data["Информация о менторах из базы"]
        info_mentor = next((item for item in dict_mentors if item['Id'] == mentor_id_tg_user_id), None)


        id_tg_user_id = info_mentor.get("IdTgUserId")  # айди ментора в таблице users
        id_mentor = info_mentor.get("Id")
        subject = info_mentor.get("Subject")
        mentor_name = info_mentor.get("Name")

        # list_user_mentor = (await select_mentors_from_db())["Наставники из таблицы users"]
        list_user_mentor = current_mentors_data["Наставники из таблицы users"]

        tg_user_id = next((dict["TgUserId"] for dict in list_user_mentor if dict["Id"] == id_tg_user_id), None)

        try:
            user_name = callback.from_user.username

            await bot.send_message(chat_id=tg_user_id, text=f"🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n"
                                                            f"@{user_name} подал заявку на работу с "
                                                            f"вами по направлению «{subject}»",
                                   disable_web_page_preview=True)

            await asyncio.sleep(0.5)

            await bot.send_message(callback.from_user.id, f"<b>Готово ✅</b>\n\n"
                                                          f"Наставник свяжется с вами в личной переписке "
                                                          f"в течение суток.\n"
                                                          f"Пожалуйста, не забудьте оставить "
                                                          f"открытыми личные сообщения🙏",
                                   disable_web_page_preview=True)

            id_user = (await work_database.select_user()).get('Id') # айди ученика из таблицы users

            await work_database.insert_query(InsertQuery=f"INSERT INTO mentorrecords(UserID, MentorUserID, MentorID, Subject) " 
                                           f"VALUES ({id_user}, {mentor_id_tg_user_id}, {id_mentor},'{subject}');") # заносим запись пользователя к ментору в таблицу

        except Exception as ex:
            await bot.send_message(chat_id=callback.from_user.id, text=f"К сожалению, наставник покинул место работы, "
                                                                       f"в скором времени он будет удалён",
                                   disable_web_page_preview=True)
            await asyncio.sleep(0.5)
            for admin in admins: #рассылкаем всем админам
                await bot.send_message(chat_id=admin, text=f"Наставник {mentor_name} отключил бота "
                                                                           f"и уведомления с платформы",
                                       disable_web_page_preview=True)
                await asyncio.sleep(0.5)

    else:
        await bot.send_message(callback.from_user.id, f"Ощибка! База менторов ещё выгружается\n"
                                                      f"Это займет некоторое время⏳",
                               disable_web_page_preview=True)