from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_choose = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Выбор 1', callback_data='choose_1'),
            InlineKeyboardButton(text='Выбор 2', callback_data='choose_2'),
        ],
    ],
)
ikb_check = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='check_in'),
            InlineKeyboardButton(text='Нет', callback_data='check_out'),
        ],
    ],
)
