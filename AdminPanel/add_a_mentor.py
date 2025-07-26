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

from AdminPanel.Admins import admins


bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()


class NewMentor(StatesGroup): #хранилище машино состояний для добавления ментора
    mentor_name = State() #Имя наставника
    card_name = State() #Имя карточки
    id_tg_user_id = State() #айди юзера в базе
    photo_mentor = State() #фото наставника
    description_mentor = State() #описание на карточке
    directions = State() #направление работы
    price = State() #стоимоить
    google_drive = State() #ссылка на гугл диск

@router.message(F.text == 'Отмена')
async def cancellation(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           f"<b>{message.from_user.first_name}</b>, "
                           f"добро пожаловать в бота по наставничеству\n\n"
                           f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                           reply_markup=kb.main_menu)
    await state.clear()  # очищаем состояние

@router.callback_query(F.data == 'Добавить карточку')
async def new_mentor(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Напишите фамилию и имя наставника "
                           f"либо нажмите «Отмена», чтобы вернуться в меню",
                           reply_markup=kb.cancellation)
    await state.set_state(NewMentor.mentor_name)

@router.message(NewMentor.mentor_name)
async def new_mentor_name(message: Message, state: FSMContext):
    if len(message.text) > 35:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное имя, пожалуйста, напишите короче")
    else:
        await state.update_data(OfficialName=message.text)
        data = await state.get_data()
        await bot.send_message(message.from_user.id,
                               "Напишите имя карточки")
        await state.set_state(NewMentor.card_name)

import re
def is_english(text): #проверка, чтобы имя карточки было написано английскими буквам
    return bool(re.match('^[A-Za-z0-9_]+$', text))

@router.message(NewMentor.card_name)
async def new_mentor_card_name(message: Message, state: FSMContext):
    if is_english(text=message.text):
        admin_bd = DatabaseClass(TgUserID=message.from_user.id)
        name_check = await admin_bd.select_rows(SelectQuery=f"SELECT Id FROM mentors WHERE "
                                                      f"Name = '/{message.text}' "
                                                      f"AND Activity = 1;")

        if len(name_check) == 0: #ментора с такой карточкой нет в базе, поэтому всё подходит и идём дальше
            if len(message.text) > 35:
                await bot.send_message(message.from_user.id,
                                       "Слишком длинное имя карточки, пожалуйста, напишите короче")
            else:
                await state.update_data(CardName=message.text)
                await bot.send_message(message.from_user.id,
                                       "Напишите id пользователя")
                await state.set_state(NewMentor.id_tg_user_id)
        else:
            await bot.send_message(message.from_user.id,
                                   "Ментор с такой карточкой уже существует. Придумайте другое название карточки")

    else:
        await bot.send_message(message.from_user.id,
                                   "Имя картоточки пишется только на английском языке, "
                                   "не должно содеражть пробелов и лишних символов")


@router.message(NewMentor.id_tg_user_id)
async def new_mentor_id(message: Message, state: FSMContext):
    # Проверяем, что сообщение состоит только из цифр
    if re.match('^[0-9]+$', message.text):
        mentor_db = DatabaseClass(TgUserID=int(message.text))

        if await mentor_db.check_user_in_the_list() == True:
            id_user_mentor = (await mentor_db.select_user()).get('Id')
            await state.update_data(IdUserMentor=id_user_mentor)
            await bot.send_message(message.from_user.id,
                                   "Пришлите фотографию наставника")
            await state.set_state(NewMentor.photo_mentor)

        else:
            await bot.send_message(message.from_user.id,
                                   "Пользователь с таким id "
                                   "не является активным. Введите другое id")

    else:
        await bot.send_message(message.from_user.id,
                               "id должно состоять состоять только из цифр")


@router.message(lambda message: message.content_type != ContentType.PHOTO, NewMentor.photo_mentor)
async def handle_no_photo(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Пожалуйста, пришлите фото наставника")
@router.message(lambda message: message.content_type == ContentType.PHOTO, NewMentor.photo_mentor)
async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(PhotoMentor=message.photo[-1].file_id)
    await bot.send_message(message.from_user.id,
                           f"Напишите описание на карточке наставника.\n"
                           f"Максимальная длина - 150 символов")
    await state.set_state(NewMentor.description_mentor)


@router.message(NewMentor.description_mentor)
async def description_mentor(message: Message, state: FSMContext):
    if len(message.text) > 150:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное описание, пожалуйста, напишите короче")
    else:
        await state.update_data(DescriptionMentor=message.text)
        str_directions = ", ".join(list(dict_directions.values()))
        await bot.send_message(message.from_user.id,
                               f"{str_directions}")
        await bot.send_message(message.from_user.id,
                               f"☝️Список направлений. Напишите, по какому направлению "
                               f"будет работать наставник")
        await state.set_state(NewMentor.directions)


@router.message(NewMentor.directions)
async def directions(message: Message, state: FSMContext):
    if message.text in list(dict_directions.values()): #проверка на то, что направление написано админом правильно и существует в списке
        await state.update_data(Directions=message.text)
        await bot.send_message(message.from_user.id,
                               f"Теперь напишите стоимость занятия с ментором\n"
                               f"Пример: «1500р за занятие» или «250.000р за курс/ведение»")
        await state.set_state(NewMentor.price)
    else:
        await bot.send_message(message.from_user.id,
                               f"Такого направления нет в списке, напишите другое")



@router.message(NewMentor.price)
async def price(message: Message, state: FSMContext):
    if len(message.text) > 35:
        await bot.send_message(message.from_user.id,
                               f"Слишком длинное сообщение, пожалуйста, напишите короче")
    else:
        await state.update_data(Price=message.text)
        await bot.send_message(message.from_user.id,
                               f"Теперь пришлите ссылку на гугл диск")

        await state.set_state(NewMentor.google_drive)

# Регулярное выражение для проверки ссылки на Google Drive
GOOGLE_DRIVE_LINK_PATTERN = re.compile(r'https://docs.google.com/\S+')

@router.message(NewMentor.google_drive)
async def google_drive(message: Message, state: FSMContext):
    if GOOGLE_DRIVE_LINK_PATTERN.match(message.text):
        await state.update_data(GoogleDrive=message.text)

        data = await state.get_data()

        new_mentor_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Создать', callback_data='Создать ментора')],
            [InlineKeyboardButton(text='Сбросить', callback_data='Отмена поста')]
        ])

        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['PhotoMentor'],
                             caption=f"<b>{data['OfficialName']}</b>\n{data['CardName']}\n"
                                     f"Направление: {data['Directions']}\n\n"
                                     f"{data['DescriptionMentor']}\n"
                                     f"<a href='{data['GoogleDrive']}'>подробнее..</a>\n\n"
                                     f"Стоимость: {data['Price']}",
                             reply_markup=new_mentor_kb)
    else:
        await bot.send_message(message.from_user.id,
                               f"Это не ссылка на гугл диск. Пришлите повторно")


@router.callback_query(F.data == 'Создать ментора')
async def created_mantor(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    data = await state.get_data()

    admin_bd = DatabaseClass(TgUserID=callback.from_user.id)

    try:
        import random
        await admin_bd.insert_query(InsertQuery=f"INSERT INTO mentors(OfficialName, Name, IdTgUserId, Photo, Description, Subject, Price, DetailedInformation, CallOrder) " 
                                       f"VALUES ('{data['OfficialName']}', '/{data['CardName']}', {data['IdUserMentor']}, '{data['PhotoMentor']}', '{data['DescriptionMentor']}', '{data['Directions']}', '{data['Price']}', '{data['GoogleDrive']}', {random.randint(30, 500)});")
        await bot.send_message(callback.from_user.id,
                               f"Новый наставник успешно создан👌",
                               reply_markup=kb.main_menu)
    except Exception as ex:
        await bot.send_message(callback.from_user.id,
                               f"Ошибка. Не удалось загрузить наставника на платформу",
                               reply_markup=kb.main_menu)

    await state.clear()  # очищаем состояние

