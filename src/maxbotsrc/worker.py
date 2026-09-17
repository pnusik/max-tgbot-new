import asyncio
import json
import maxapi
import redis.asyncio as aioredis

from .funcshon import text_message_sender, file_message_sender

async def worker(bot: maxapi.Bot, redisclient: aioredis.Redis):
    try:
        while True:
            text_message = await redisclient.blpop("text_message_in_MAX", timeout=1.0)
    
            if text_message:
                queue_name, task_json = text_message
    
                task = json.loads(task_json)
                print(task)
   
                await text_message_sender(bot, task['author'], task['text'])

            file_message = await redisclient.blpop("file_message_in_MAX", timeout=1.0)

            if file_message:
                queue_name, task_json = file_message
                    
                task: dict = json.loads(task_json)
                print(task)
                   
                await file_message_sender(bot, task.get("file_path", ""), task.get("author", ""), task.get("max_id", ""))

            await asyncio.sleep(0.1)
    finally:
        await redisclient.aclose()