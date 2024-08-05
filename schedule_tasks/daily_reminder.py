import aiosqlite
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..constants import DATABASE_PATH

scheduler = AsyncIOScheduler()


async def get_user_ids() -> list[int]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            user_ids = [user[0] for user in await cursor.fetchall()]
            return user_ids


async def send_daily_reminder(bot):
    user_ids = await get_user_ids()
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, "Не забудьте проверить уведомления!")
        except Exception:
            return


def setup_scheduler(bot):
    scheduler.add_job(
        send_daily_reminder,
        CronTrigger(hour=9, minute=00),
        args=[bot],
        id='daily_reminder',
        name='Send daily reminder at 9 AM',
        replace_existing=True
    )
    scheduler.start()
