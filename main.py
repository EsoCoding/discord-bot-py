import os
import dotenv

from os.path import join, dirname

from modules.MusicBot import MusicBot
from modules.logger import Logger



# Importing Logger outside main function to improve readability and performance
logger = Logger()

def check_env():

    # Load.env file.
    try:
        env = join(dirname(__file__), '.env')
        Logger.info("Loaded .env file")
    except:
        Logger.error("Failed loading .env file")
        exit()


def main() -> None:
    """
    The main function of the program.
    """

    Logger.info("Starting music bot.")

    #Check if env exists, else exit
    check_env()

    # Encapsulate bot actions inside the main function.
    bot: MusicBot = MusicBot()

    # Replacing os.getenv with os.environ[], specifying the full path to the token if necessary.
    bot.client.run(os.environ["DISCORD_BOT_TOKEN"])


if __name__ == "__main__":
    """
    Entry point of the program.
    """

    main()