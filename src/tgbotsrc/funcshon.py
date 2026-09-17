import aiogram
from aiogram import types
from config.config import TG_cofnig
import filetype
import os

config = TG_cofnig()

async def message_sender(bot: aiogram.Bot, autor: str, msg: str, chat_id: int, thread_id: int | None):
    text = f">{autor}:\n{msg}"
    await bot.send_message(chat_id=chat_id, text=text, message_thread_id=thread_id)


async def file_message_sender(bot: aiogram.Bot, file_path: str, file_name: str, autor: str):
    text = f">{autor}:"
    kind = filetype.guess(file_path)
    print(kind)
    mime_type = kind.mime if kind else None

    if mime_type and mime_type.startswith('image/'):
        await bot.send_photo(
            chat_id=config.Chat_id,
            message_thread_id=config.Thread_id,
            photo=types.FSInputFile(file_path, file_name),
            caption=text)

    else:
        await bot.send_document(
            chat_id=config.Chat_id,
            message_thread_id=config.Thread_id,
            document=types.FSInputFile(file_path, file_name),
            caption=text)

    if os.path.exists(file_path):
        os.remove(file_path)