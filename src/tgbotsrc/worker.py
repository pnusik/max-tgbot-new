import asyncio
import json
import aiogram
import redis.asyncio as aioredis

from .funcshon import message_sender, file_message_sender

async def worker(bot: aiogram.Bot, redisclient: aioredis.Redis):
    try:
        while True:
            message = await redisclient.blpop("text_message_in_TG", timeout=1.0)
    
            if message:
                queue_name, task_json = message
    
                task = json.loads(task_json)
                print(task)
   
                await message_sender(bot, task['author'], task['text'])


            file_message = await redisclient.blpop("file_message_in_TG", timeout=1.0)
            if file_message:
                queue_name, task_json = file_message

                task = json.loads(task_json)
                print(task)

                await file_message_sender(bot, task['file_path'], task["file_name"], task["author"])


            await asyncio.sleep(0.1)
    finally:
        await redisclient.aclose()