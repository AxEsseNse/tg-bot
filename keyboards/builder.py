from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_username_rkb(username: str):
    builder = ReplyKeyboardBuilder()
    builder.button(text=username)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
