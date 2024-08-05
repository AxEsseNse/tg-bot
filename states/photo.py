from aiogram.fsm.state import State, StatesGroup


class PhotoForm(StatesGroup):
    photo = State()
