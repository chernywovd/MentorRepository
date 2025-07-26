from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
from aiogram.filters import Command
from keyboards import keyboard as kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


from Functions.SearchDescription import search_direction

from Database.Database import DatabaseClass

bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()

class Post(StatesGroup): #хранилище машино состояний для создания постов
    text_post = State() #текст поста
    photo_post = State()  # фото поста
    video_post = State() #видео поста


type_post = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Текстовый', callback_data='Текстовый пост')],

     [InlineKeyboardButton(text='Видео', callback_data='Видео пост'),
      InlineKeyboardButton(text='Фото', callback_data='Фото пост')],

    [InlineKeyboardButton(text='Отмена', callback_data='Отмена поста')]
])

from AdminPanel.Admins import admins
@router.message(Command(commands=["post"]), F.from_user.id.in_(admins))
async def post(message: Message, state: FSMContext):
    await state.clear()  # на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Выберите, какого формата создать пост',
                           reply_markup=type_post)

@router.callback_query(F.data == 'Отмена поста')
async def close(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"<b>{callback.from_user.first_name}</b>, "
                           f"добро пожаловать в бота по наставничеству\n\n"
                           f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                           reply_markup=kb.main_menu)



#Текстовая заявка
@router.callback_query(F.data == 'Текстовый пост')
async def give(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Напишите текст поста")
    await state.set_state(Post.text_post)

@router.message(Post.text_post)
async def text(message: Message, state: FSMContext):
    if len(message.text) > 2000:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное сообщение, пожалуйста, напишите короче")
    else:
        await state.update_data(text=message.text)

        data = await state.get_data()

        place_a_post = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Опубликовать✈️', callback_data=f"Опубликовать"),
             InlineKeyboardButton(text='Отменить❌', callback_data='Отмена поста')],
        ])

        if data.get('photo') is None and data.get('video') is None: #пост написн только текстом
            await bot.send_message(message.from_user.id, f"{data['text']}",
                                   reply_markup=place_a_post)
        elif data.get('photo') is not None: # пост с картиной
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=data['photo'],
                                 caption=f"{data['text']}",
                                 reply_markup=place_a_post)
            # await bot.send_message(chat_id=message.from_user.id, text=f"{data['photo']}")
        elif data.get('video') is not None: # пост с видео
            await bot.send_video(chat_id=message.from_user.id,
                                 video=data['video'],
                                 caption=f"{data['text']}",
                                 reply_markup=place_a_post)


#Фото пост
@router.callback_query(F.data == 'Фото пост')
async def give(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Пришлите фото для поста")
    await state.set_state(Post.photo_post)
@router.message(lambda message: message.content_type != ContentType.PHOTO, Post.photo_post)
async def handle_no_photo(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Пожалуйста, пришлите фото или картинку")
@router.message(lambda message: message.content_type == ContentType.PHOTO, Post.photo_post)
async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await bot.send_message(message.from_user.id,
                           f"Напишите текст поста")
    await state.set_state(Post.text_post)



#Видео пост
@router.callback_query(F.data == 'Видео пост')
async def give(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Пришлите видео для поста")
    await state.set_state(Post.video_post)
@router.message(lambda message: message.content_type != ContentType.VIDEO, Post.video_post)
async def handle_no_video(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Пожалуйста, пришлите видео")
@router.message(lambda message: message.content_type == ContentType.VIDEO, Post.video_post)
async def handle_video(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)
    await bot.send_message(message.from_user.id,
                           f"Напишите текст поста")
    await state.set_state(Post.text_post)


#Отправка поста пользователям
@router.callback_query(F.data == 'Опубликовать')
async def send(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    user_bd = DatabaseClass(TgUserID=callback.from_user.id)

    all_users = await user_bd.select_rows(SelectQuery=f"SELECT TgUserId FROM users WHERE "
                                                      f"Activity = 1;")
    data = await state.get_data()

    await bot.send_message(callback.from_user.id,
                           f"Отправка пользователям запущена✅")

    if data.get('photo') is None and data.get('video') is None:  # пост написн только текстом
        for tg_user_id in all_users:
            try:
                await bot.send_message(chat_id=tg_user_id['TgUserId'], text=f"{data['text']}")
            except Exception as ex:
                # Ставим Activity = 1 пользователю
                await user_bd.update_query(UpdateQuery=f"UPDATE users SET Activity = 0 "
                                                       f"WHERE TgUserId = {tg_user_id['TgUserId']};")
            await asyncio.sleep(0.5)

    elif data.get('photo') is not None:  # пост с картиной
        for tg_user_id in all_users:
            try:
                await bot.send_photo(chat_id=tg_user_id['TgUserId'],
                                     photo=data['photo'],
                                     caption=f"{data['text']}")
            except Exception as ex:
                # Ставим Activity = 1 пользователю
                await user_bd.update_query(UpdateQuery=f"UPDATE users SET Activity = 0 "
                                                       f"WHERE TgUserId = {tg_user_id['TgUserId']};")
            await asyncio.sleep(0.5)

    elif data.get('video') is not None:  # пост с видео
        for tg_user_id in all_users:
            try:
                await bot.send_video(chat_id=tg_user_id['TgUserId'],
                                     video=data['video'],
                                     caption=f"{data['text']}")
            except Exception as ex:
                # Ставим Activity = 1 пользователю
                await user_bd.update_query(UpdateQuery=f"UPDATE users SET Activity = 0 "
                                                       f"WHERE TgUserId = {tg_user_id['TgUserId']};")
            await asyncio.sleep(0.5)

    await state.clear() #очищаем состояние