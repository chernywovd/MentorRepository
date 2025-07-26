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



bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()



from AdminPanel.Admins import admins
@router.message(Command(commands=["oper_on_mentor"]), F.from_user.id.in_(admins))
async def newmentor(message: Message, state: FSMContext):
    await state.clear()  # на всякий случай очищаем состояние

    await bot.send_message(message.from_user.id, 'Выберите действие, которое хотите совершить над карточкой ментора',
                           reply_markup=kb.operation_on_mentor)