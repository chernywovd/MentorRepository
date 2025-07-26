from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
from Sub.Subjects import dict_directions
from keyboards import keyboard as kb
from Database.Database import DatabaseClass
import asyncio
import re


bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()


class UpdateMentor(StatesGroup): #хранилище машино состояний для изменения карточки ментора
    mentor_name = State() #Имя наставника
    new_name = State() #новое имя наставника
    new_name_card = State() #новое имя карточки
    user_id = State() #новый айди
    new_photo = State() #новое фото
    new_description = State() #новое описание
    new_subject = State() #новое направление
    new_price = State() #новая цена
    new_google_drive = State() #новая ссылка на гугл диск







from AdminPanel.Admins import admins
@router.callback_query(F.data == 'Изменить карточку')
async def upd_mentor(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Напишите имя карточки для изменения "
                           f"либо нажмите «Отмена», чтобы вернуться в меню",
                           reply_markup=kb.cancellation)
    await state.set_state(UpdateMentor.mentor_name)
@router.message(F.text == 'Отмена')
async def cancellation(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           f"<b>{message.from_user.first_name}</b>, "
                           f"добро пожаловать в бота по наставничеству\n\n"
                           f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                           reply_markup=kb.main_menu)
    await state.clear()  # очищаем состояние


@router.message(UpdateMentor.mentor_name)
async def mentor_name(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                          f"Name = '/{message.text}' "
                                                          f"AND Activity = 1;")
    if len(mentor) == 0:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Такой карточки нет. Введите другое имя "
                                    f"либо нажмите /start, чтобы вернуться в меню")
    else:
        for info in mentor:  # проходимся по списку, но в нём находится один наставник
            mentor_photo = info['Photo']
            mentor_id = info['Id']
            mentor_name = info['OfficialName']
            mentor_card_name = info['Name']
            subject = info['Subject']
            description = info['Description']
            detailed_information = info['DetailedInformation']
            price = info['Price']

            update_men = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                 InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                 InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                 InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                 InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
            ])

            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=mentor_photo,
                                 caption=f"<b>{mentor_name}</b> ({subject})\n"
                                         f"{mentor_card_name[1:]}\n\n"
                                         f"{description}\n"
                                         f"<a href='{detailed_information}'>подробнее..</a>\n"
                                         f"Стоимость: {price}",
                                 reply_markup=update_men)
            await asyncio.sleep(0.5)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Выберите, что нужно изменить в карточке👆")






#Изменение имени ментора
@router.callback_query((F.data)[:11] == 'Имя ментора')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[11:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Напишите новое имя наставника")
    await state.set_state(UpdateMentor.new_name)
@router.message(UpdateMentor.new_name)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    if len(message.text) > 35:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное имя, пожалуйста, напишите короче")
    else:
        try:
            data = await state.get_data()
            await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET OfficialName = '{message.text}' "
                                                           f"WHERE Id = {data['MentorID']};")

            mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                            f"Id = {data['MentorID']};")

            for info in mentor:  # проходимся по списку, но в нём находится один наставник
                mentor_photo = info['Photo']
                mentor_id = info['Id']
                mentor_name = info['OfficialName']
                mentor_card_name = info['Name']
                subject = info['Subject']
                description = info['Description']
                detailed_information = info['DetailedInformation']
                price = info['Price']

                update_men = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                     InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                     InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                     InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                    [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                     InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                    [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                ])

                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=mentor_photo,
                                     caption=f"<b>{mentor_name}</b> ({subject})\n"
                                             f"{mentor_card_name[1:]}\n\n"
                                             f"{description}\n"
                                             f"<a href='{detailed_information}'>подробнее..</a>\n"
                                             f"Стоимость: {price}",
                                     reply_markup=update_men)
                await asyncio.sleep(0.5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
        except Exception:
            await bot.send_message(message.from_user.id,
                                   "Не удалось обновить карочтку. Попробуйте позже")

        await state.clear()  # очищаем состояние










#Изменение имени карточки ментора
@router.callback_query((F.data)[:12] == 'Имя карточки')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[12:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Напишите новое имя карточки")
    await state.set_state(UpdateMentor.new_name_card)
@router.message(UpdateMentor.new_name_card)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    # Проверяем, что сообщение состоит из англ букв и цифр
    if re.match('^[A-Za-z0-9_]+$', message.text):
        name_check = await admin_db.select_rows(SelectQuery=f"SELECT Id FROM mentors WHERE "
                                                            f"Name = '/{message.text}' "
                                                            f"AND Activity = 1;")
        if len(name_check) == 0:  # ментора с такой карточкой нет в базе, поэтому всё подходит и идём дальше
            if len(message.text) > 35:
                await bot.send_message(message.from_user.id,
                                       "Слишком длинное имя карточки, пожалуйста, напишите короче")
            else:
                try:
                    data = await state.get_data()
                    await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET Name = '/{message.text}' "
                                                                   f"WHERE Id = {data['MentorID']};")

                    mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                                    f"Id = {data['MentorID']};")

                    for info in mentor:  # проходимся по списку, но в нём находится один наставник
                        mentor_photo = info['Photo']
                        mentor_id = info['Id']
                        mentor_name = info['OfficialName']
                        mentor_card_name = info['Name']
                        subject = info['Subject']
                        description = info['Description']
                        detailed_information = info['DetailedInformation']
                        price = info['Price']

                        update_men = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                             InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                            [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                             InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                            [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                             InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                            [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                             InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                            [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                        ])

                        await bot.send_photo(chat_id=message.from_user.id,
                                             photo=mentor_photo,
                                             caption=f"<b>{mentor_name}</b> ({subject})\n"
                                                     f"{mentor_card_name[1:]}\n\n"
                                                     f"{description}\n"
                                                     f"<a href='{detailed_information}'>подробнее..</a>\n"
                                                     f"Стоимость: {price}",
                                             reply_markup=update_men)
                        await asyncio.sleep(0.5)
                        await bot.send_message(chat_id=message.from_user.id,
                                               text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
                except Exception:
                    await bot.send_message(message.from_user.id,
                                           "Не удалось обновить карочтку. Попробуйте позже")

                await state.clear()  # очищаем состояние
        else:
            await bot.send_message(message.from_user.id,
                                   "Ментор с такой карточкой уже существует. Придумайте другое название карточки")
    else:
        await bot.send_message(message.from_user.id,
                               "Имя картоточки пишется только на английском языке, "
                               "не должно содеражть пробелов и лишних символов")














#Изменение id ментора
@router.callback_query((F.data)[:10] == 'Tg_user_id')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[10:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Напишите новое id наставника")
    await state.set_state(UpdateMentor.user_id)
@router.message(UpdateMentor.user_id)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    # Проверяем, что сообщение состоит только из цифр
    if re.match('^[0-9]+$', message.text):
        mentor_db = DatabaseClass(TgUserID=int(message.text))
        if await mentor_db.check_user_in_the_list() == True: # пользователь с таким айди есть в базе
            id_user_mentor = (await mentor_db.select_user()).get('Id')
            try:
                data = await state.get_data()
                await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET IdTgUserId = '{id_user_mentor}' "
                                                        f"WHERE Id = {data['MentorID']};")

                mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                                f"Id = {data['MentorID']};")

                for info in mentor:  # проходимся по списку, но в нём находится один наставник
                    mentor_photo = info['Photo']
                    mentor_id = info['Id']
                    mentor_name = info['OfficialName']
                    mentor_card_name = info['Name']
                    subject = info['Subject']
                    description = info['Description']
                    detailed_information = info['DetailedInformation']
                    price = info['Price']

                    update_men = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                         InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                        [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                         InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                        [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                         InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                        [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                         InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                        [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                    ])

                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=mentor_photo,
                                         caption=f"<b>{mentor_name}</b> ({subject})\n"
                                                 f"{mentor_card_name[1:]}\n\n"
                                                 f"{description}\n"
                                                 f"<a href='{detailed_information}'>подробнее..</a>\n"
                                                 f"Стоимость: {price}",
                                         reply_markup=update_men)
                    await asyncio.sleep(0.5)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
            except Exception:
                await bot.send_message(message.from_user.id,
                                       "Не удалось обновить карочтку. Попробуйте позже")

            await state.clear()  # очищаем состояние

        else:
            await bot.send_message(message.from_user.id,
                                   "Пользователь с таким id "
                                   "не является активным. Введите другое id")


    else:
        await bot.send_message(message.from_user.id,
                               "id должно состоять состоять только из цифр")














#Изменение id ментора
@router.callback_query((F.data)[:13] == 'Фото карточки')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[13:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Пришлите новую фотографию")
    await state.set_state(UpdateMentor.new_photo)
@router.message(lambda message: message.content_type != ContentType.PHOTO, UpdateMentor.new_photo)
async def handle_no_photo(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Это не фото. Пожалуйста, пришлите фото наставника")
@router.message(lambda message: message.content_type == ContentType.PHOTO, UpdateMentor.new_photo)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    try:
        data = await state.get_data()
        await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET Photo = '{message.photo[-1].file_id}' "
                                                f"WHERE Id = {data['MentorID']};")

        mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                        f"Id = {data['MentorID']};")

        for info in mentor:  # проходимся по списку, но в нём находится один наставник
            mentor_photo = info['Photo']
            mentor_id = info['Id']
            mentor_name = info['OfficialName']
            mentor_card_name = info['Name']
            subject = info['Subject']
            description = info['Description']
            detailed_information = info['DetailedInformation']
            price = info['Price']

            update_men = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                 InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                 InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                 InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                 InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
            ])

            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=mentor_photo,
                                 caption=f"<b>{mentor_name}</b> ({subject})\n"
                                         f"{mentor_card_name[1:]}\n\n"
                                         f"{description}\n"
                                         f"<a href='{detailed_information}'>подробнее..</a>\n"
                                         f"Стоимость: {price}",
                                 reply_markup=update_men)
            await asyncio.sleep(0.5)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
    except Exception:
        await bot.send_message(message.from_user.id,
                               "Не удалось обновить карочтку. Попробуйте позже")

    await state.clear()  # очищаем состояние















#Изменение описания карточки
@router.callback_query((F.data)[:8] == 'Описание')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[8:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Напишите новое описание карточки")
    await state.set_state(UpdateMentor.new_description)
@router.message(UpdateMentor.new_description)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    if len(message.text) > 150:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное описание, пожалуйста, напишите короче")
    else:
        try:
            data = await state.get_data()
            await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET Description = '{message.text}' "
                                                           f"WHERE Id = {data['MentorID']};")

            mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                            f"Id = {data['MentorID']};")

            for info in mentor:  # проходимся по списку, но в нём находится один наставник
                mentor_photo = info['Photo']
                mentor_id = info['Id']
                mentor_name = info['OfficialName']
                mentor_card_name = info['Name']
                subject = info['Subject']
                description = info['Description']
                detailed_information = info['DetailedInformation']
                price = info['Price']

                update_men = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                     InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                     InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                     InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                    [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                     InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                    [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                ])

                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=mentor_photo,
                                     caption=f"<b>{mentor_name}</b> ({subject})\n"
                                             f"{mentor_card_name[1:]}\n\n"
                                             f"{description}\n"
                                             f"<a href='{detailed_information}'>подробнее..</a>\n"
                                             f"Стоимость: {price}",
                                     reply_markup=update_men)
                await asyncio.sleep(0.5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
        except Exception:
            await bot.send_message(message.from_user.id,
                                   "Не удалось обновить карочтку. Попробуйте позже")

        await state.clear()  # очищаем состояние
















#Изменение направления
@router.callback_query((F.data)[:11] == 'Направление')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[11:])

    str_directions = ", ".join(list(dict_directions.values()))
    await bot.send_message(callback.from_user.id,
                           f"{str_directions}")

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"☝️Список направлений. Напишите, по какому направлению "
                           f"будет работать наставник")
    await state.set_state(UpdateMentor.new_subject)
@router.message(UpdateMentor.new_subject)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    if message.text not in list(dict_directions.values()): #проверка на то, что направление написано админом правильно и существует в списке
        await bot.send_message(message.from_user.id,
                               "Такого направления нет в списке, напишите другое")
    else:
        try:
            data = await state.get_data()
            await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET Subject = '{message.text}' "
                                                           f"WHERE Id = {data['MentorID']};")

            mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                            f"Id = {data['MentorID']};")

            for info in mentor:  # проходимся по списку, но в нём находится один наставник
                mentor_photo = info['Photo']
                mentor_id = info['Id']
                mentor_name = info['OfficialName']
                mentor_card_name = info['Name']
                subject = info['Subject']
                description = info['Description']
                detailed_information = info['DetailedInformation']
                price = info['Price']

                update_men = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                     InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                     InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                     InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                    [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                     InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                    [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                ])

                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=mentor_photo,
                                     caption=f"<b>{mentor_name}</b> ({subject})\n"
                                             f"{mentor_card_name[1:]}\n\n"
                                             f"{description}\n"
                                             f"<a href='{detailed_information}'>подробнее..</a>\n"
                                             f"Стоимость: {price}",
                                     reply_markup=update_men)
                await asyncio.sleep(0.5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
        except Exception:
            await bot.send_message(message.from_user.id,
                                   "Не удалось обновить карочтку. Попробуйте позже")

        await state.clear()  # очищаем состояние














#Изменение цены
@router.callback_query((F.data)[:4] == 'Цена')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[4:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Напишите новую стоимость занятия с ментором\n"
                           f"Пример: «1500р за занятие» или «250.000р за курс/ведение»")
    await state.set_state(UpdateMentor.new_price)
@router.message(UpdateMentor.new_price)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    if len(message.text) > 35:
        await bot.send_message(message.from_user.id,
                               f"Слишком длинное сообщение, пожалуйста, напишите короче")
    else:
        try:
            data = await state.get_data()
            await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET Price = '{message.text}' "
                                                           f"WHERE Id = {data['MentorID']};")

            mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                            f"Id = {data['MentorID']};")

            for info in mentor:  # проходимся по списку, но в нём находится один наставник
                mentor_photo = info['Photo']
                mentor_id = info['Id']
                mentor_name = info['OfficialName']
                mentor_card_name = info['Name']
                subject = info['Subject']
                description = info['Description']
                detailed_information = info['DetailedInformation']
                price = info['Price']

                update_men = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                     InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                     InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                     InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                    [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                     InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                    [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                ])

                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=mentor_photo,
                                     caption=f"<b>{mentor_name}</b> ({subject})\n"
                                             f"{mentor_card_name[1:]}\n\n"
                                             f"{description}\n"
                                             f"<a href='{detailed_information}'>подробнее..</a>\n"
                                             f"Стоимость: {price}",
                                     reply_markup=update_men)
                await asyncio.sleep(0.5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
        except Exception:
            await bot.send_message(message.from_user.id,
                                   "Не удалось обновить карочтку. Попробуйте позже")

        await state.clear()  # очищаем состояние










#Изменение ссылки на гугл диск
@router.callback_query((F.data)[:9] == 'Гугл диск')
async def update_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await state.update_data(MentorID=callback.data[9:])

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Пришлите новую ссылку на гугл диск")
    await state.set_state(UpdateMentor.new_google_drive)

# Регулярное выражение для проверки ссылки на Google Drive
GOOGLE_DRIVE_LINK_PATTERN = re.compile(r'https://docs.google.com/\S+')

@router.message(UpdateMentor.new_google_drive)
async def update_mentor_men(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    if GOOGLE_DRIVE_LINK_PATTERN.match(message.text):
        try:
            data = await state.get_data()
            await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET DetailedInformation = '{message.text}' "
                                                           f"WHERE Id = {data['MentorID']};")

            mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                            f"Id = {data['MentorID']};")

            for info in mentor:  # проходимся по списку, но в нём находится один наставник
                mentor_photo = info['Photo']
                mentor_id = info['Id']
                mentor_name = info['OfficialName']
                mentor_card_name = info['Name']
                subject = info['Subject']
                description = info['Description']
                detailed_information = info['DetailedInformation']
                price = info['Price']

                update_men = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Имя', callback_data=f"Имя ментора{mentor_id}"),
                     InlineKeyboardButton(text='Им. карт.', callback_data=f"Имя карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Id', callback_data=f"Tg_user_id{mentor_id}"),
                     InlineKeyboardButton(text='Фото', callback_data=f"Фото карточки{mentor_id}")],

                    [InlineKeyboardButton(text='Описание', callback_data=f"Описание{mentor_id}"),
                     InlineKeyboardButton(text='Направление', callback_data=f"Направление{mentor_id}")],

                    [InlineKeyboardButton(text='Цена', callback_data=f"Цена{mentor_id}"),
                     InlineKeyboardButton(text='Гугл диск', callback_data=f"Гугл диск{mentor_id}")],

                    [InlineKeyboardButton(text='Выйти', callback_data='Отмена поста')]
                ])

                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=mentor_photo,
                                     caption=f"<b>{mentor_name}</b> ({subject})\n"
                                             f"{mentor_card_name[1:]}\n\n"
                                             f"{description}\n"
                                             f"<a href='{detailed_information}'>подробнее..</a>\n"
                                             f"Стоимость: {price}",
                                     reply_markup=update_men)
                await asyncio.sleep(0.5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Выберите, нужно ли ещё что-то изменить в карточке👆")
        except Exception:
            await bot.send_message(message.from_user.id,
                                   "Не удалось обновить карочтку. Попробуйте позже")

        await state.clear()  # очищаем состояние

    else:
        await bot.send_message(message.from_user.id,
                               f"Это не ссылка на гугл диск. Пришлите повторно")

