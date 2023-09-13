# This class represents the MusicBot
from modules.bot import Bot
from modules.logger import Logger

logging = Logger()
        
if __name__ == "__main__":
    bot = Bot()
    bot.start()