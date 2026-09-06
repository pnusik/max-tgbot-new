import redis.asyncio as aioredis
import json

redis_client = None

async def get_redis_connection():
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url(
            "redis://localhost:6379", 
            decode_responses=True
        )
    return redis_client

async def redis_send(queue_name, data):
    global redis_client
    await redis_client.rpush(queue_name, json.dumps(data, ensure_ascii=False))