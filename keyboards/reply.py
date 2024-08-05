from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

rkb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/help'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню',
)
remove_rkb = ReplyKeyboardRemove()
