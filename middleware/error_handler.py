from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            error_message = 'Произошла ошибка, попробуйте позже'
            if isinstance(event, Message):
                await event.answer(error_message)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(error_message)
            return None
