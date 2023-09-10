import os

from pathlib import Path

from discord import Intents
from discord.ext.commands import Bot
from modules.MusicBot import MusicBot
from modules.logger import Logger
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    bot = Bot(
    command_prefix=os.getenv("DISCORD_BOT_PREFIX"),
    intents=Intents.all(),
    help_command=None,)
    bot.add_cog(MusicBot())

