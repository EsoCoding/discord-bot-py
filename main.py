import os

from pathlib import Path
from modules.MusicBot import MusicBot
from modules.logger import Logger
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    """
    The main function of the program.
    """
    # Log the start of the program
    Logger().info("Starting music bot.")

    # Initialize bot and run.
    bot: MusicBot = MusicBot()
    bot.client.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    """
    Entry point of the program.
    """

    main()
