import aiosqlite
from aiogram import html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from ..constants import DATABASE_PATH
from ..keyboards import ikb_choose, rkb_start
from ..routers import commands_router


@commands_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(html.bold('Добро пожаловать в наш бот!'), reply_markup=rkb_start)


@commands_router.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer(
        '<b>Доступные команды:</b>\n'
        '   • /start - Начало работы с ботом\n'
        '   • /help - Просмотр всех доступных команд\n'
        '   • /echo - Возвращает ваше сообщение (Пример: /echo фиксик)\n'
        '   • /photo - Узнать разрешение фотографии\n'
        '   • /choose - Выбор из 2 вариантов\n'
        '   • /user_info - Регистрация пользователя\n'
        '   • /users - Получить список пользователей\n'
        '   • /weather - Получить прогноз погоды в городе',
        parse_mode='HTML'
    )


@commands_router.message(Command('echo'))
async def command_echo(message: Message) -> None:
    msg = message.text
    if len(msg) < 7:
        await message.answer('Вы не ввели никакого сообщения')
    else:
        await message.answer(msg[6:])


@commands_router.message(Command('choose'))
async def command_choose(message: Message) -> None:
    await message.answer('Выберите действие из меню', reply_markup=ikb_choose)


@commands_router.message(Command('users'))
async def command_users(message: Message) -> None:
    answer_string = 'Список всех пользователей:'
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            async for user in cursor:
                answer_string += '\n{user_id}: {name} - {age}'.format(
                    user_id=user[0],
                    name=user[1],
                    age=user[2],
                )
    await message.answer(answer_string)
