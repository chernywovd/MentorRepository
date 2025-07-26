import asyncio
import datetime
from aiogram import F, Router
from aiogram import Bot, Dispatcher
from Config import exemplyar_bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types
from keyboards import keyboard as kb
from Database.Database import DatabaseClass

bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()

# async def set_default_commands(dp):
#     await dp.bot.set_my_commands([
#         types.BotCommand("start", "Запустить бота")
#     ])

admins = [6027246732]
@router.message(Command(commands=["start", "help"]))
async def start_comand(message: Message, state: FSMContext):
    await state.clear()  # на всякий случай очищаем состояние

    commands = [
        BotCommand(command="start", description="Перезапустить бота")
    ]
    await bot.set_my_commands(commands)

    user_bd = DatabaseClass(TgUserID=message.from_user.id)

    if message.text == '/start':
        if await user_bd.check_user_in_the_list() == True:

            #Ставим Activity = 1 пользователю
            id_user = (await user_bd.select_user()).get('Id')
            await user_bd.update_query(UpdateQuery=f"UPDATE users SET Activity = 1 "
                                                   f"WHERE Id = {id_user};")


            await bot.send_message(message.from_user.id,
                                   f"<b>{message.from_user.first_name}</b>, "
                                   f"добро пожаловать в бота по наставничеству\n\n"
                                   f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                                   reply_markup=kb.main_menu)
        else:
            await user_bd.insert_user() #заносим пользователя в базу
            await bot.send_message(message.from_user.id,
                                   f"<b>{message.from_user.first_name}</b>, "
                                   f"добро пожаловать в бота по наставничеству\n\n"
                                   f"Если желаете изучить площадку, перейдите в раздел👇\n<b>«Инструкция по платформе🌍»</b>",
                                   reply_markup=kb.main_menu)


