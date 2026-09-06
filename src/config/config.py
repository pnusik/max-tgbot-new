class Global_config:
    def __init__(self):
        self.path_to_download_folder = "/home/andrey/Desktop/progects/Telegrammaxbot/downloads"

class TG_cofnig(Global_config):
    def __init__(self):
        super().__init__()
        self.BOT_TOKEN="8111294889:AAFNZaTTlsLHlCF1kJfIb9naVEBgXELY6T4"
        self.Chat_id=-1003994286063
        self.Thread_id=2
        self.react_to_sucsess = "👍"

class MAX_config(Global_config):
    def __init__(self):
        super().__init__()
        self.BOT_TOKEN="f9LHodD0cOJRre0JlJmw0Op5lwZmV-6WkE6EFdv99e2FAxJ_QO98_S3RLO7X3zjumSwNLNQwaC6iR-0Kvkw8"
        self.Chat_id=-78472421107172