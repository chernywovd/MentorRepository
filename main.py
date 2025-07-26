import asyncio
from aiogram import Bot, Dispatcher
from Config import exemplyar_bot
from handlers import start_handler, choice_direction, search_mentor, suggestions_and_complaints
from AdminPanel import become_a_mentor, posts, delete_a_mentor, add_a_mentor, update_a_mentor, oper_on_mentor
from Database.random_mentor import scheduler_mix
from Database.import_mentors import scheduler_update_data_mentors
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = exemplyar_bot.bot
dp = Dispatcher()


async def main():
    dp.include_router(start_handler.router) #старт
    dp.include_router(posts.router) #для постов
    dp.include_router(oper_on_mentor.router) #команда для произведения операций над менторами
    dp.include_router(delete_a_mentor.router) #для удаления меторов
    dp.include_router(add_a_mentor.router) #для добавления меторов
    dp.include_router(update_a_mentor.router)  # для обновления карточки
    dp.include_router(choice_direction.router) #выбор напавления
    dp.include_router(become_a_mentor.router) #подача заявки на работу
    dp.include_router(search_mentor.router) #поиск ментора
    dp.include_router(suggestions_and_complaints.router)  # Жалобы и предложения

    await scheduler_update_data_mentors() #раз в 1.5 минуты вытаскиваем данные о менторах и заносим их в словарь
    await scheduler_mix() #перемешка наставников раз в сутки

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())