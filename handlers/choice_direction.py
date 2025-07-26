from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import keyboard as kb

import datetime

from Database.Database import DatabaseClass





bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()


@router.message(F.text=='Найти наставника🔎')
async def search_mentor(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Выберите направление наставничества',
                           reply_markup=kb.type_of_mentor)

@router.message(F.text=='Назад⬅️')
async def back(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id,
                           f"<b>{message.from_user.first_name}</b>, "
                           f"добро пожаловать в бота по наставничеству\n\n"
                           f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                           reply_markup=kb.main_menu)

@router.message(F.text=='Назад↩️')
async def back(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id,
                           'Выберите направление наставничества',
                           reply_markup=kb.type_of_mentor)


@router.message(F.text=='Репетиторы👨‍🏫')
async def tutors(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Здесь вы можете как воспользоваться услугами репетиторов, так и приобрести услуги '
                                                 'выполненяй домашних заданий, написаний эссе, дипломов и иных научных работ',
                           reply_markup=kb.tutors_type)


@router.message(F.text=='Тренеры💪')
async def trainers(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Выберите спортивное направление',
                           reply_markup=kb.sports_type)
@router.message(F.text=='Танцы💃')
async def dancing(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Выберите направление танцев',
                           reply_markup=kb.dancing)
@router.message(F.text=='Назад🏃')
async def trainers(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Выберите спортивное направление',
                           reply_markup=kb.sports_type)





@router.message(F.text=='Менторы по заработку🤑')
async def earn(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Здесь вы можете как воспользоваться услугами специалистов, '
                                                 'так и пройти их обучение, чтобы самостоятельно добиться '
                                                 'результатов в выбранной нише',
                           reply_markup=kb.earn_type)



@router.message(F.text=='Иностранные яз🏌️‍♂️')
async def languages(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Выберите язык, который хотите изучить",
                           reply_markup=kb.languages)
@router.message(F.text=='Бьюти-сфера💅')
async def beauty(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Выберите, в какой бьюти-сфере вы хотите стать мастером",
                           reply_markup=kb.beauty_sphere)
@router.message(F.text=='Моделинг🛫')
async def modeling(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Выберите, чему хотите обучиться",
                           reply_markup=kb.modeling)

@router.message(F.text=='Назад🔙')
async def back(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Здесь вы можете как воспользоваться услугами репетиторов, так и приобрести услуги "
                                                 "выполнений домашних заданий, написаний эссе, дипломов и иных научных работ",
                           reply_markup=kb.tutors_type)
@router.message(F.text=='Назад🚶')
async def back(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Здесь вы можете как воспользоваться услугами специалистов, '
                                                 'так и пройти их обучение, чтобы самостоятельно добиться '
                                                 'результатов в выбранной нише',
                           reply_markup=kb.earn_type)

@router.message(F.text=='Искусство🎭')
async def art(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Выберите направление искусства",
                           reply_markup=kb.art)
@router.message(F.text=='Музыка🎶')
async def art2(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Выберите музыкальное направление",
                           reply_markup=kb.art2)
@router.message(F.text=='Назад')
async def art2(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, "Выберите направление искусства",
                           reply_markup=kb.art)



@router.message(F.text=='Наставники по здоровью👩‍⚕️')
async def earn(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Выберите направление',
                           reply_markup=kb.health)


