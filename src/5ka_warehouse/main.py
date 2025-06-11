from core.dispatcher import dp, bot
import asyncio

from middlewares.db import DataBaseSession

from database.engine import create_db, session_maker, drop_db


async def on_startup(bot):
    # await drop_db()
    await create_db()

async def main() -> None:
    dp.startup.register(on_startup)
    
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())