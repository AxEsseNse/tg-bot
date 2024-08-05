import aiosqlite
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..constants import DATABASE_PATH
from ..routers import user_info_router
from ..states import UserForm


async def update_user_data(user_id: int, data: dict):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET name = ?, age = ? WHERE id = ?',
            (data['name'], data['age'], user_id)
        )
        await db.commit()


@user_info_router.callback_query(UserForm.check, F.data.in_(['check_in', 'check_out']))
async def process_callback_check(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'check_in':
        data = await state.get_data()
        user_id = callback_query.from_user.id
        await update_user_data(user_id=user_id, data=data)

        await state.clear()
        await callback_query.message.answer('Ваше имя: {name}\nВаш возраст: {age}'.format(
            name=data['name'],
            age=data['age']
        ))
        await callback_query.message.delete()
    else:
        await state.clear()
        await callback_query.answer('Данные вашего аккаунта не изменены')
        await callback_query.message.delete()
