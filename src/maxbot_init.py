from maxapi import Bot, Dispatcher
from db.redis import get_redis_connection
import asyncio
from config.config import MAX_config
from maxbotsrc.hendlers import router
from maxbotsrc.worker import worker
from db.sqldb import init_db

config = MAX_config()
async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)

    redis = await get_redis_connection()
    await init_db()

    await asyncio.gather(
            dp.start_polling(bot),
            worker(bot, redis)
        )

if __name__ == "__main__":
    asyncio.run(main())