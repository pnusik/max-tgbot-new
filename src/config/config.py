from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Global_config:
    def __init__(self):
        self.path_to_download_folder = "/home/andrey/Desktop/progects/Telegrammaxbot/downloads"

class TG_cofnig(Global_config):
    def __init__(self):
        super().__init__()
        self.BOT_TOKEN = getenv("TG_BOT_TOKEN")
        self.Chat_id = int(getenv("TG_CHAT_ID")) # pyright: ignore[reportArgumentType]
        self.Thread_id=2
        self.react_to_sucsess = "👍"

class MAX_config(Global_config):
    def __init__(self):
        super().__init__()
        self.BOT_TOKEN = getenv("MAX_BOT_TOKEN")
        self.Chat_id = int(getenv("MAX_CHAT_ID")) # pyright: ignore[reportArgumentType]

