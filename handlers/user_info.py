import aiosqlite
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..constants import DATABASE_PATH
from ..keyboards import create_username_rkb, ikb_check, remove_rkb
from ..routers import user_info_router
from ..states import UserForm


async def check_user_exist(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT id FROM users WHERE id == ?', (user_id,)) as cursor:
            data = await cursor.fetchone()
            return data


async def save_user_data(user_id: int, data: dict):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (user_id, data['name'], data['age']))
        await db.commit()


@user_info_router.message(Command('user_info'))
async def command_user_info(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)
    await message.answer(
        'Введите ваше имя',
        reply_markup=create_username_rkb(message.from_user.first_name)
    )


@user_info_router.message(UserForm.name)
async def user_form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserForm.age)
    await message.answer('Теперь введите ваш возраст', reply_markup=remove_rkb)


@user_info_router.message(UserForm.age)
async def user_form_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        user_id = message.from_user.id
        user_exist = await check_user_exist(user_id)

        if user_exist:
            await state.set_state(UserForm.check)
            await message.answer(
                'Ваш аккаунт уже зарегистрирован в системе. Вы желаете изменить данные?',
                reply_markup=ikb_check,
            )
            return

        data = await state.get_data()
        await save_user_data(user_id=user_id, data=data)

        await state.clear()
        await message.answer(f'Ваше имя: {data['name']}\nВаш возраст: {data['age']}')
    else:
        await message.answer('Возраст может быть только числом')
