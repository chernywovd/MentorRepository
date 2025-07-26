# import asyncio
#
# from aiogram import F, Router
# from aiogram import Bot, Dispatcher
# import exemplyar_bot
# from aiogram.filters import CommandStart, Command, CommandObject
# from aiogram.types import Message
#
#
#
# bot = exemplyar_bot.bot
#
# router = Router()
#
# @router.message(Command('help'))
# async def hepl_comand(message: Message):
#     await bot.send_message(message.from_user.id, "Этот бот предназначен для оптимизации "
#                                                  "подсчётов личных расходов")
