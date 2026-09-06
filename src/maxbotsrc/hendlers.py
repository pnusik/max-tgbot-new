from maxapi import Router, types, F
from db.redis import redis_send
from config.config import MAX_config

config = MAX_config()
router = Router()

@router.message_created(F.message.body.text)
async def message_hendler(message: types.MessageCreated):
    data = {
            "author": message.from_user.full_name,
            "text": message.message.body.text,
    }
    await redis_send("text_message_in_TG", data)
    await message.mark_seen()


@router.message_created(F.message.body.attachments)
async def message_hendler_file(message: types.MessageCreated):
    url = message.message.body.attachments[-1].payload.url

    attachment = message.message.body.attachments[-1]

    path = await router.bot.download_file(
                            url=url, 
                            destination=config.path_to_download_folder,
                            filename=attachment.payload.token)

    await redis_send("file_message_in_TG", 
                    {"file_path": str(path), 
                    "file_name": attachment.payload.token,
                    "author": message.from_user.full_name})

    await message.mark_seen()