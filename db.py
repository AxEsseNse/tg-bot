import aiosqlite


async def create_db():
    async with aiosqlite.connect('bot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
        )
        ''')
        await db.commit()
