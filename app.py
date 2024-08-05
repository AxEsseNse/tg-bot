import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiohttp import web

from tg_bot.callbacks import *  # noqa: F403, F401
from tg_bot.constants import BOT_TOKEN
from tg_bot.db import create_db
from tg_bot.handlers import *  # noqa: F403, F401
from tg_bot.middleware import ErrorHandlerMiddleware
from tg_bot.routers import (
    choose_router,
    commands_router,
    message_router,
    photo_router,
    user_info_router,
    weather_router,
)
from tg_bot.schedule_tasks import setup_scheduler

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
app = web.Application()
webhook_path = f'/{BOT_TOKEN}'

dp.message.middleware(ErrorHandlerMiddleware())
dp.include_routers(
    commands_router,
    user_info_router,
    photo_router,
    choose_router,
    weather_router,
    message_router,
)

setup_scheduler(bot)


async def set_webhook():
    webhook_uri = f'https://94d6-37-252-91-220.ngrok-free.app{webhook_path}'
    await bot.set_webhook(
        webhook_uri
    )


async def on_startup(_):
    await create_db()
    await set_webhook()


async def on_shutdown(_):
    await bot.session.close()
    if 'sessions' in app:
        for session in app['sessions']:
            await session.close()

    await asyncio.sleep(0.5)


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]
    if token == BOT_TOKEN:
        request_data = await request.json()
        update = Update(**request_data)

        await dp.feed_update(bot, update)

        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post(f'/{BOT_TOKEN}', handle_webhook)


if __name__ == '__main__':
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(
        app=app,
        host='0.0.0.0',
        port=8080,
    )
