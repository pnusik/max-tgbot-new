from aiogram import Router, types, F, Bot
from aiogram.types import ReactionTypeEmoji
from db.redis import redis_send
from config.config import TG_cofnig
import os


config = TG_cofnig()
router = Router()

@router.message(F.text)
async def handle_msg(message: types.Message):
    if message.chat.id == config.Chat_id and message.message_thread_id == config.Thread_id:
        if not message.text:
            message.reply("ТЕХИНФО: Не найден текст сообщения")
        data = {
            "author": message.from_user.full_name,
            "text": message.text,
            "message_id": message.message_id
        }
        await redis_send("text_message_in_MAX", data)
        await message.react(reaction=[
                    ReactionTypeEmoji(emoji=config.react_to_sucsess)
                    ])

@router.message(F.photo | F.document)
async def handle_photo(message: types.Message, bot: Bot):
    if message.chat.id == config.Chat_id and message.message_thread_id == config.Thread_id:
        
        if message.photo:
            file = message.photo[-1]
            file_path = f"{config.path_to_download_folder}/{file.file_id}.jpg"

        if message.document:
            file = message.document
            _, extension = os.path.splitext(message.document.file_name)
            file_path = f"{config.path_to_download_folder}/{file.file_id}{extension}"


        await bot.download(file=file.file_id,
                        destination=file_path)

        
        data = {"file_path": file_path, "author": message.from_user.full_name}
        await redis_send("file_message_in_MAX", data)
        await message.react(reaction=[
            ReactionTypeEmoji(emoji=config.react_to_sucsess)
            ])