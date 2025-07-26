from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import keyboard as kb
from Database.Database import DatabaseClass
from AdminPanel.Admins import admins



bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()


class DelMentor(StatesGroup): #хранилище машино состояний для удаления ментора
    mentor_name = State() #Имя наставника



@router.message(F.text == 'Отмена')
async def cancellation(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           f"<b>{message.from_user.first_name}</b>, "
                           f"добро пожаловать в бота по наставничеству\n\n"
                           f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                           reply_markup=kb.main_menu)
    await state.clear()  # очищаем состояние

@router.callback_query(F.data == 'Удалить карточку')
async def del_mentor(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Напишите имя карточки для удаления "
                           f"либо нажмите «Отмена», чтобы вернуться в меню",
                           reply_markup=kb.cancellation)
    await state.set_state(DelMentor.mentor_name)

@router.message(DelMentor.mentor_name)
async def del_mentor_name(message: Message, state: FSMContext):
    admin_db = DatabaseClass(TgUserID=message.from_user.id)

    mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                          f"Name = '/{message.text}' "
                                                          f"AND Activity = 1;")
    if len(mentor) == 0: # такой карточки нет
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Такой карточки нет. Введите другое имя "
                                    f"либо нажмите /start, чтобы вернуться в меню")
    else:
        for info in mentor:  # проходимся по списку, но в нём находится один наставник
            mentor_photo = info['Photo']
            mentor_id = info['Id']
            mentor_name = info['OfficialName']
            description = info['Description']

            del_men = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Удалить', callback_data=f"Удаление карточки с id{mentor_id}"),
                 InlineKeyboardButton(text='Отмена', callback_data='Отмена поста')]
            ])

            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=mentor_photo,
                                 caption=f"<b>{mentor_name}</b>\n\n"
                                         f"{description}\n",
                                 reply_markup=del_men)




@router.callback_query((F.data)[0:22] == 'Удаление карточки с id')
async def del_mentor_men(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    admin_db = DatabaseClass(TgUserID=callback.from_user.id)

    mentor_id_from_table_mentors = (callback.data)[22:] # айди ментора в таблице mentors
    data_mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                    f"Id = {mentor_id_from_table_mentors};")
    data_mentor = data_mentor[0] # т.к. в списке одна запись, обращаемся напрямую к ней

    #Ставим статус активности карточки 0
    await admin_db.update_query(UpdateQuery=f"UPDATE mentors SET Activity = 0 "
                                                   f"WHERE Id = {mentor_id_from_table_mentors};")


    #Проверяем, если у ментора более нет карточек, то ставим статус его активности 0, если карточки ещё есть, то удаляется только та, которая была введена админом
    id_mentor_from_table_mentor = data_mentor['IdTgUserId']
    check_mentor = await admin_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                    f"IdTgUserId = {id_mentor_from_table_mentor} "
                                                          f"AND Activity = 1;")
    if len(check_mentor) == 0:
        # await admin_db.update_query(UpdateQuery=f"UPDATE listmentor SET Activity = 0 "
        #                                            f"WHERE Id = {mentor_id_from_table_ListMentor};")
        await bot.send_message(callback.from_user.id,
                               f"Наставник удалён❗️\n"
                               f"больше карточек он не имеет")
    else:
        await bot.send_message(callback.from_user.id,
                               f"Карточка удалена❗️\n"
                               f"данный наставник имеет ещё карточки по другим направлениям")


    await state.clear() #очищаем состояние