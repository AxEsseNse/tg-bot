from aiogram.types import Message

from ..routers import message_router


@message_router.message()
async def unknown_messages(message: Message):
    await message.answer('Недопустимая команда')
