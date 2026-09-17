from maxapi import Router, types, F
from db.redis import redis_send
from config.config import MAX_config
from db.sqldb import get_tg_chat_and_thread_ids

config = MAX_config()
router = Router()

@router.message_created(F.message.body.text)
async def message_hendler(message: types.MessageCreated):
    tg_chat_id, tg_thread_id = await get_tg_chat_and_thread_ids(message.chat.chat_id) # type: ignore

    if not tg_chat_id:
        print("id не найден в макс боте")
        return

    data = {
            "author": message.from_user.full_name, # type: ignore
            "text": message.message.body.text, # type: ignore
            "chat_id": tg_chat_id,
            "tg_thread_id": tg_thread_id
    }
    await redis_send("text_message_in_TG", data)
    await message.mark_seen()


@router.message_created(F.message.body.attachments)
async def message_hendler_file(message: types.MessageCreated):
    assert message.message.body is not None
    
    url = message.message.body.attachments[-1].payload.url # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess, reportOptionalSubscript]

    attachment = message.message.body.attachments[-1] # pyright: ignore[reportOptionalSubscript]

    path = await router.bot.download_file( # type: ignore
                            url=url,  # pyright: ignore[reportArgumentType]
                            destination=config.path_to_download_folder,
                            filename=attachment.payload.token)  # type: ignore

    await redis_send("file_message_in_TG", 
                    {"file_path": str(path), 
                    "file_name": attachment.payload.token, # type: ignore
                    "author": message.from_user.full_name}) # type: ignore

    await message.mark_seen()