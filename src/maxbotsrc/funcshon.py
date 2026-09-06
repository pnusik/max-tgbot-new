import maxapi
from config.config import MAX_config
from maxapi.types import InputMedia
import os

config = MAX_config()

async def text_message_sender(bot: maxapi.Bot, autor: str, msg: str):
    text = f">{autor}:\n{msg}"
    msg = await bot.send_message(chat_id=config.Chat_id, text=text)
    if msg:
        return True

async def file_message_sender(bot: maxapi.Bot, file_path: str, autor: str):
    text = f">{autor}:"
    await bot.send_message(
        chat_id=config.Chat_id,
        text=text,
        attachments=[
            InputMedia(path=file_path)
            ]
        )

    if os.path.exists(file_path):
        os.remove(file_path)