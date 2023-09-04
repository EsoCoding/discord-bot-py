import os

from pathlib import Path
from modules.MusicBot import MusicBot
from modules.logger import Logger


def main() -> None:
    """
    The main function of the program.
    """
    # Log the start of the program
    Logger().info("Starting music bot.")

    # Set the working directory to the directory of this file.
    os.chdir(Path(__file__).parent)

    # Initialize bot and run.
    bot: MusicBot = MusicBot()
    bot.client.run(token=os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    """
    Entry point of the program.
    """

    main()
