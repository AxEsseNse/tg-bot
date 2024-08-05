from aiogram import F
from aiogram.types import CallbackQuery

from ..routers import choose_router


@choose_router.callback_query(F.data.in_(['choose_1', 'choose_2']))
async def process_callback_choose(callback_query: CallbackQuery):
    if callback_query.data == 'choose_1':
        await callback_query.answer('Вы выбрали Выбор 1')
    else:
        await callback_query.answer('Вы выбрали Выбор 2')
