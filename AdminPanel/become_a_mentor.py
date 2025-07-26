from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import keyboard as kb
import asyncio
from AdminPanel.Admins import admins
from Database.Database import DatabaseClass


bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()



class SubmitAnApplication(StatesGroup): #хранилище машино состояний для подачи заявки на менторство
    mentor_name = State() #Имя наставника
    direction = State() #направление наставничества
    experience = State() #опыт работы




@router.message(F.text=='Стать наставником👨‍🔬')
async def become_ment(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id, 'Если Вы '
                                                 'готовы обучить чему-либо и '
                                                 'хотите присоединиться к команде '
                                                 'наставников на нашей платформе, '
                                                 'пожалуйста, подайте заявку и пошагово '
                                                 'пройдите несколько простых вопросов',
                           reply_markup=kb.become_ment)

@router.message(F.text=='Подать заявку✍️')
async def statement(message: Message, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    statement = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Начать', callback_data=f"Подать заявку"), InlineKeyboardButton(text='Отмена', callback_data='Отмена поста')],
            ])
    await bot.send_message(message.from_user.id, 'Сейчас нужно будет составить анкету, '
                                                 'ответив на несколько вопросов. Начинаем?',
                           reply_markup=statement)



@router.callback_query(F.data == 'Отмена готовой заявки')
async def close(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Если Вы '
                                                 'готовы обучить чему-либо и '
                                                 'хотите присоединиться к команде '
                                                 'наставников на нашей платформе, '
                                                 'пожалуйста, подайте заявку и пошагово '
                                                 'пройдите несколько простых вопросов',
                           reply_markup=kb.become_ment)



@router.callback_query(F.data == 'Подать заявку')
async def give(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id,
                           f"Пожалуйста, напишите своё имя. Как мы можем к Вам обращаться?")
    await state.set_state(SubmitAnApplication.mentor_name)

@router.message(SubmitAnApplication.mentor_name)
async def name(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное имя, пожалуйста, напишите короче")
    else:
        user_bd = DatabaseClass(TgUserID=message.from_user.id)

        await state.update_data(name=message.text)
        await state.update_data(user_name=f"@{message.from_user.username}")
        await state.update_data(id=f"{message.from_user.id}") # id пользователя в базе


        await bot.send_message(message.from_user.id,
                               "Хорошо. Теперь напишите одно или "
                               "несколько направлений, по которым хотите работать")
        await state.set_state(SubmitAnApplication.direction)  # Заправшиваем направление наставничества

@router.message(SubmitAnApplication.direction)
async def direction(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное сообщение, пожалуйста, напишите короче")
    else:
        await state.update_data(direction=message.text)
        await bot.send_message(message.from_user.id,
                               "Расскажите о себе и своём опыте в профессии или преподавании")
        await state.set_state(SubmitAnApplication.experience)  #запрашиваем инфу об опыте

@router.message(SubmitAnApplication.experience)
async def experience(message: Message, state: FSMContext):
    if len(message.text) > 1000:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное сообщение, пожалуйста, напишите короче")
    else:
        await state.update_data(experience=message.text)
        data = await state.get_data()

        send_or_cancel = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отправить🛫', callback_data=f"Отправить заявку"),
             InlineKeyboardButton(text='Отменить❌', callback_data='Отмена готовой заявки')],
        ])
        await bot.send_message(message.from_user.id, f"<b>Направления:</b>\n{data['direction']}\n\n"
                                                     f"<b>Информация о Вас:</b>\n{data['experience']}\n\n"
                                                     f"<b>Автор</b>👉{data['user_name']}, {data['name']}",
                               reply_markup=send_or_cancel)



@router.callback_query(F.data == 'Отправить заявку')
async def send(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Благодарим за заявку🙏\n"
                           f"Мы свяжемся с вами в течение 1-2 суток."
                           f"\nПожалуйста, не забудьте оставить открытыми личные сообщения")
    await asyncio.sleep(0.5)

    data = await state.get_data()
    for admin in admins: #рассылкаем всем админам
        sent_message = await bot.send_message(chat_id=admin,
                               text=f"Заявка на менторство🔥🔥🔥🔥🔥\n\n"
                                    f"<b>Направления:</b>\n{data['direction']}\n\n"
                                                         f"<b>Информация о менторе:</b>\n{data['experience']}\n\n"
                                                         f"<b>Автор</b>👉{data['user_name']}, {data['name']}\n"
                                                         f"<b>id пользователя:</b> {data['id']}")
        # Закрепляем сообщение
        await bot.pin_chat_message(chat_id=admin, message_id=sent_message.message_id)
        await asyncio.sleep(0.5)

    await state.clear() #очищаем состояние
