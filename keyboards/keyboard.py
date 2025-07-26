from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Найти наставника🔎')],
    [KeyboardButton(text='Стать наставником👨‍🔬')],
    [KeyboardButton(text='Инструкция по платформе🌍')],
    [KeyboardButton(text='Предложения и жалобы📝')]],
    resize_keyboard=True)


become_ment = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Подать заявку✍️')],
    [KeyboardButton(text='Назад⬅️')]
],
    resize_keyboard=True)


type_of_mentor = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Менторы по заработку🤑')],
    [KeyboardButton(text='Репетиторы👨‍🏫'), KeyboardButton(text='Тренеры💪')],
    [KeyboardButton(text='Искусство🎭'), KeyboardButton(text='Наставники по здоровью👩‍⚕️')],
    [KeyboardButton(text='Назад⬅️')]],
    resize_keyboard=True)


tutors_type = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Математика🔢'), KeyboardButton(text='Физика🪂')],
    [KeyboardButton(text='Русский яз🇷🇺'), KeyboardButton(text='Иностранные яз🏌️‍♂️')],
    [KeyboardButton(text='История🦣'), KeyboardButton(text='Обществознание🏦')],
    [KeyboardButton(text='Литература📚'), KeyboardButton(text='Биология🌳')],
    [KeyboardButton(text='Химия👩‍🔬'), KeyboardButton(text='География🗺')],
    [KeyboardButton(text='Информатика💻'), KeyboardButton(text='Логопеды🗣')],
    [KeyboardButton(text='Назад↩️')]],
    resize_keyboard=True)


languages = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Английский яз🇬🇧'), KeyboardButton(text='Итальянский яз🇮🇹')],
    [KeyboardButton(text='Французский яз🇫🇷'), KeyboardButton(text='Арабский яз🇪🇬')],
    [KeyboardButton(text='Назад🔙')]],
    resize_keyboard=True)



sports_type = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Фитнес🏋️‍♂️')],
    [KeyboardButton(text='Бокс🥊')],
    [KeyboardButton(text='Пилатес и йога🧘‍♀️')],
    [KeyboardButton(text='Танцы💃')],
    [KeyboardButton(text='Назад↩️')]],
    resize_keyboard=True)

health = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Психологи🗣')],
    [KeyboardButton(text='Нутрициологи🥝')],
    [KeyboardButton(text='Консультации беременным🤰')],
    [KeyboardButton(text='Назад↩️')]],
    resize_keyboard=True)


dancing = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Хип-хоп')],
    [KeyboardButton(text='Джаз-фанк'), KeyboardButton(text='Хай-хилс')],
    [KeyboardButton(text='Крамп'), KeyboardButton(text='Брейк-данс')],
    [KeyboardButton(text='Электро'), KeyboardButton(text='Дансхолл')],
    [KeyboardButton(text='Назад🏃')]],
    resize_keyboard=True)




earn_type = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Арбитраж траф📲'), KeyboardButton(text='Искусство продаж💸')],
    [KeyboardButton(text='Маркетплейсы📦'), KeyboardButton(text='Крипта🪙')],
    [KeyboardButton(text='Программирование👨‍💻'), KeyboardButton(text='Монтаж 🎞')],
    [KeyboardButton(text='СММ(лич. бренд)🤳'), KeyboardButton(text='Веб-дизайн🏙')],
    [KeyboardButton(text='Предпринимательство🤵‍♂️'), KeyboardButton(text='Инвестиции💸')],
    [KeyboardButton(text='Видеография🎥'), KeyboardButton(text='Проф фотограф📸')],
    [KeyboardButton(text='Бьюти-сфера💅'), KeyboardButton(text='Моделинг🛫')],
    [KeyboardButton(text='Массаж💆‍♂️'), KeyboardButton(text='Барбер💇‍♂️')],
    [KeyboardButton(text='Назад↩️')]],
    resize_keyboard=True)

beauty_sphere = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Ногти💅'), KeyboardButton(text='Брови🖌')],
    [KeyboardButton(text='Ресницы👁'), KeyboardButton(text='Волосы👩‍🦳')],
    [KeyboardButton(text='Визаж и макияж🤩'), KeyboardButton(text='Моментальный загар💁🏽‍♀️')],
    [KeyboardButton(text='Назад🚶')]],
    resize_keyboard=True)

modeling = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Позирование и дефиле🔗')],
    [KeyboardButton(text='Назад🚶')]],
    resize_keyboard=True)

# programming = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Python'), KeyboardButton(text='PHP')],
#     [KeyboardButton(text='Java'), KeyboardButton(text='JavaScript')],
#     [KeyboardButton(text='C++'), KeyboardButton(text='C#')],
#     [KeyboardButton(text='Kotlin'), KeyboardButton(text='Swift')],
#     [KeyboardButton(text='GO'), KeyboardButton(text='Devops')],
#     [KeyboardButton(text='Назад🚶')]],
#     resize_keyboard=True, input_field_placeholder='Выберите')


art = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Актёрское мастерство🕺')],
    [KeyboardButton(text='Рисование🎨'), KeyboardButton(text='Музыка🎶')],
    [KeyboardButton(text='Назад↩️')]],
    resize_keyboard=True)

art2 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Пение🎤'), KeyboardButton(text='Битмейкинг🎵')],
    [KeyboardButton(text='Флейта🪄'), KeyboardButton(text='Гитара🎸')],
    [KeyboardButton(text='Фортепиано🎹'), KeyboardButton(text='Скрипка🎻')],
    [KeyboardButton(text='Назад')]],
    resize_keyboard=True)


cancellation = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отмена')]],
    resize_keyboard=True)





operation_on_mentor = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить', callback_data='Добавить карточку')],
        [InlineKeyboardButton(text='Изменить', callback_data='Изменить карточку'), InlineKeyboardButton(text='Удалить', callback_data='Удалить карточку')],
        [InlineKeyboardButton(text='Отмена', callback_data='Отмена поста')]
    ])


suggestion_or_complaint = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Предложить идею', callback_data='Предложить идею')],
        [InlineKeyboardButton(text='Пожаловаться', callback_data='Пожаловаться')],
        [InlineKeyboardButton(text='Отмена', callback_data='Отмена поста')]
    ])


