from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import ReactionTypeEmoji
from db.redis import redis_send
from config.config import TG_cofnig
import os
from db.sqldb import new_chat, get_max_chat_id


config = TG_cofnig()
router = Router()


@router.message(Command("connect"))
async def connect_new_chat(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("АЛО ГДЕ АРГУМЕНТЫ?!")
        return
    await new_chat(
            message.chat.id,
            message.message_thread_id,
            int(command.args.split()[0])
            )
    await message.answer("Добавлено")



@router.message(F.text)
async def handle_msg(message: types.Message):
        if not message.text:
            await message.reply("ТЕХИНФО: Не найден текст сообщения")
            return

        max_id = await get_max_chat_id(message.chat.id, message.message_thread_id)

        if not max_id:
            await message.reply("ТЕХИНФО: Чат не найден датабэйс(кароче пишите мне, пофикшу)")
            return

        
        assert message.from_user is not None
        data = {
            "author": message.from_user.full_name,
            "text": message.text,
            "message_id": message.message_id,
            "max_id": max_id
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

            assert message.document.file_name is not None
            _, extension = os.path.splitext(message.document.file_name)
            
            file_path = f"{config.path_to_download_folder}/{file.file_id}{extension}"


        await bot.download(file=file.file_id,
                        destination=file_path)

        
        data = {"file_path": file_path, "author": message.from_user.full_name} # pyright: ignore[reportOptionalMemberAccess, reportPossiblyUnboundVariable]
        await redis_send("file_message_in_MAX", data)
        await message.react(reaction=[
            ReactionTypeEmoji(emoji=config.react_to_sucsess)
            ])