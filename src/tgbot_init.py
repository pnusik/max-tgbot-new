from aiogram import Bot, Dispatcher
from db.redis import get_redis_connection
import asyncio
from config.config import TG_cofnig
from tgbotsrc.hendlers import router
from tgbotsrc.worker import worker

config = TG_cofnig()
async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    redis = await get_redis_connection()

    await asyncio.gather(
            dp.start_polling(bot),
            worker(bot, redis)
        )

if __name__ == "__main__":
    asyncio.run(main())