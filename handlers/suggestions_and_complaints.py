from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from Config import exemplyar_bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
import asyncio
import random

from handlers.mentors import dict_directions

from keyboards import keyboard as kb
from Database.Database import DatabaseClass


bot = exemplyar_bot.bot #Взято из файла экземпляра бота, где хранится токен

router = Router()


class SuggestionsOrComplaint(StatesGroup): #хранилище машино состояний для жалоб и предложений
    text = State() #Текст жалобы или предложения
    video = State()
    photo = State()


@router.message(F.text=='Предложения и жалобы📝')
async def suggestionsorcomplaint(message: Message, state: FSMContext):
    await state.clear()  # на всякий случай очищаем состояние
    await bot.send_message(message.from_user.id,
                           f"Здесь Вы можете как предложить идею для развития проекта, "
                           f"так и подать жалобу любого характера",
                           reply_markup=kb.suggestion_or_complaint)

@router.callback_query((F.data == 'Предложить идею') | (F.data == 'Пожаловаться'))
async def suggestion(callback: CallbackQuery, state: FSMContext):
    await state.clear() #на всякий случай очищаем состояние
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    if callback.data == 'Предложить идею':
        await state.update_data(IsIdea=True)
        await bot.send_message(callback.from_user.id,
                               f"Пожалуйста, опишите Вашу идею🪶",
                               reply_markup=kb.cancellation)
    elif callback.data == 'Пожаловаться':
        await state.update_data(IsComplaint=True)
        await bot.send_message(callback.from_user.id,
                               f"Пожалуйста, опишите Вашу жалобу🪶",
                               reply_markup=kb.cancellation)

    await state.update_data(UserName=f"@{callback.from_user.username}")
    await state.set_state(SuggestionsOrComplaint.text)

@router.message(SuggestionsOrComplaint.text)
async def text_idea(message: Message, state: FSMContext):
    if len(message.text) > 2500:
        await bot.send_message(message.from_user.id,
                               "Слишком длинное сообщение, пожалуйста, напишите короче",
                                reply_markup=kb.suggestion_or_complaint)
    else:
        data = await state.get_data()
        if data.get('IsIdea') is not None:
            await state.update_data(TextIdea=message.text)
        elif data.get('IsComplaint') is not None:
            await state.update_data(TextComplaint=message.text)


        video_or_photo = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='+Видео', callback_data='+Видео'), InlineKeyboardButton(text='+Фото', callback_data='+Фото')],
        [InlineKeyboardButton(text='Пропустить', callback_data='Пропустить видео и фото')]
        ])

        await bot.send_message(message.from_user.id,
                               "Отлично! Теперь, если желаете, "
                               "прикрепите видео или фото к сообщению либо "
                               "нажмите «Пропустить»",
                               reply_markup=video_or_photo)


@router.callback_query(F.data == '+Видео')
async def video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Пожалуйста, прикрепите видео")
    await state.set_state(SuggestionsOrComplaint.video)
@router.message(lambda message: message.content_type != ContentType.VIDEO, SuggestionsOrComplaint.video)
async def handle_no_video(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Пожалуйста, пришлите видео либо нажмите «Отмена»")
@router.message(lambda message: message.content_type == ContentType.VIDEO, SuggestionsOrComplaint.video)
async def handle_video(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)

    data = await state.get_data()

    place_a_mes = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Отправить', callback_data=f"Отправить пр или жл")],
                [InlineKeyboardButton(text='Отменить', callback_data='Отмена поста')]
            ])

    if data.get('IsIdea') is not None:
        await bot.send_video(chat_id=message.from_user.id,
                             video=data['video'],
                             caption=f"{data['TextIdea']}",
                             reply_markup=place_a_mes)
    elif data.get('IsComplaint') is not None:
        await bot.send_video(chat_id=message.from_user.id,
                             video=data['video'],
                             caption=f"{data['TextComplaint']}",
                             reply_markup=place_a_mes)





@router.callback_query(F.data == '+Фото')
async def video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await bot.send_message(callback.from_user.id,
                           f"Пожалуйста, прикрепите фото")
    await state.set_state(SuggestionsOrComplaint.photo)
@router.message(lambda message: message.content_type != ContentType.PHOTO, SuggestionsOrComplaint.photo)
async def handle_no_photo(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Пожалуйста, пришлите фото либо нажмите «Отмена»")
@router.message(lambda message: message.content_type == ContentType.PHOTO, SuggestionsOrComplaint.photo)
async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)

    data = await state.get_data()

    place_a_mes = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить', callback_data=f"Отправить пр или жл")],
        [InlineKeyboardButton(text='Отменить', callback_data='Отмена поста')]
    ])

    if data.get('IsIdea') is not None:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=f"{data['TextIdea']}",
                             reply_markup=place_a_mes)
    elif data.get('IsComplaint') is not None:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=f"{data['TextComplaint']}",
                             reply_markup=place_a_mes)




@router.callback_query(F.data == 'Пропустить видео и фото')
async def skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    data = await state.get_data()

    place_a_mes = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить', callback_data=f"Отправить пр или жл")],
        [InlineKeyboardButton(text='Отменить', callback_data='Отмена поста')]
    ])

    if data.get('IsIdea') is not None:
        await bot.send_message(callback.from_user.id,
                               f"{data['TextIdea']}",
                               reply_markup=place_a_mes)
    elif data.get('IsComplaint') is not None:
        await bot.send_message(callback.from_user.id,
                               f"{data['TextComplaint']}",
                               reply_markup=place_a_mes)


@router.callback_query(F.data == 'Отправить пр или жл')
async def send(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # чтобы пропали часики
    await bot.delete_message(callback.from_user.id, callback.message.message_id)


    data = await state.get_data()

    if data.get('IsIdea') is not None:
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"Благодарим за поданную идею!\n\n"
                                    f"Мы рассмотрим Ваше предложение и дадим обратную связь🙏",
                               reply_markup=kb.main_menu)
        second = random.randint(1, 27)
        await asyncio.sleep(second)

        if data.get('video') is None and data.get('photo') is None: #идея чисто текстом
            sent_message = await bot.send_message(chat_id=893630880,
                                                  text=f"👀 Предложение от {data['UserName']}\n\n"
                                                  f"{data['TextIdea']}")
            await bot.pin_chat_message(chat_id=893630880, message_id=sent_message.message_id)  # Закрепляем сообщение

        elif data.get('video') is not None: # идея с прикрепленным видео
            sent_message = await bot.send_message(chat_id=893630880,
                                                  text=f"👀 Предложение от {data['UserName']}👇")
            await bot.send_video(chat_id=893630880,
                                 video=data['video'],
                                 caption=f"{data['TextIdea']}")
            await bot.pin_chat_message(chat_id=893630880, message_id=sent_message.message_id)  # Закрепляем сообщение

        elif data.get('photo') is not None: # идея с прикрепленной картинкой
            sent_message = await bot.send_message(chat_id=893630880,
                                                  text=f"👀 Предложение от {data['UserName']}👇")
            await bot.send_photo(chat_id=893630880,
                                 photo=data['photo'],
                                 caption=f"{data['TextIdea']}")
            await bot.pin_chat_message(chat_id=893630880, message_id=sent_message.message_id)  # Закрепляем сообщение



    elif data.get('IsComplaint') is not None:
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"Благодарим!\n\n"
                                    f"Мы рассмотрим Вашу жалобу, свяжемся с Вами и примем меры",
                               reply_markup=kb.main_menu)
        second = random.randint(1, 27)
        await asyncio.sleep(second)

        if data.get('video') is None and data.get('photo') is None:  # жалоба чисто текстом
            sent_message = await bot.send_message(chat_id=893630880,
                                                  text=f"👀 Жалоба от {data['UserName']}\n\n"
                                                       f"{data['TextComplaint']}")
            await bot.pin_chat_message(chat_id=893630880, message_id=sent_message.message_id)  # Закрепляем сообщение

        elif data.get('video') is not None:  # Жалоба с прикрепленным видео
            sent_message = await bot.send_message(chat_id=893630880,
                                                  text=f"👀 Жалоба от {data['UserName']}👇")
            await bot.send_video(chat_id=893630880,
                                 video=data['video'],
                                 caption=f"{data['TextComplaint']}")
            await bot.pin_chat_message(chat_id=893630880, message_id=sent_message.message_id)  # Закрепляем сообщение

        elif data.get('photo') is not None:  # Жалоба с прикрепленной картинкой
            sent_message = await bot.send_message(chat_id=893630880,
                                                  text=f"👀 Жалоба от {data['UserName']}👇")
            await bot.send_photo(chat_id=893630880,
                                 photo=data['photo'],
                                 caption=f"{data['TextComplaint']}")
            await bot.pin_chat_message(chat_id=893630880, message_id=sent_message.message_id)  # Закрепляем сообщение


