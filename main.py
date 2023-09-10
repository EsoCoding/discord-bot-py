import os
from dotenv import load_dotenv


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


import os

def main() -> None:
    """
    The main function of the program.
    """

    # Log a message indicating that the music bot is being launched.
    Logger.info("Launching music bot.")

    # Check if the necessary environment variables exist.
    check_env()

    # Create an instance of the MusicBot class.
    bot: MusicBot = MusicBot()

    # Run the bot by passing the Discord bot token as an argument.
    bot.client.run(os.environ["DISCORD_BOT_TOKEN"])


if __name__ == "__main__":
    """
    Entry point of the program.
    """

    # Run the main function
    main()