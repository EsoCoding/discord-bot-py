# Import the os and discord libraries
import os
import discord

# Import discord class and Intents class
# from the discord library
from discord import Intents
from discord.ext import commands

# import custom modules
from modules.Fetcher import Fetcher
from modules.Logger import Logger


# This class represents the MusicBot
class MusicBot:
    # This is the constructor of the MusicBot class
    def __init__(self):
        # Create a Discord bot with the specified command prefix and intents
        self.client = commands.Bot(
            command_prefix=os.getenv("DISCORD_BOT_PREFIX"), intents=Intents.all()
        )

        # Event handler for when the bot is ready
        @self.client.event
        async def on_ready():
            # Log that the bot is logged in and print it to the console
            Logger.info(f"Bot is now logged in as {self.client.user}")
            print(f"Bot is now logged in as {self.client.user}")

            # Set the bot's presence to "Music Downloader Bot"
            await self.client.change_presence(
                activity=discord.Game(name="Music Downloader Bot")
            )

        # Command handler for the "dt" command
        @self.client.command()
        async def dt(ctx, arg):
            try:
                # Log the received command and the author
                Logger.info(f"Received command {ctx.command} from {ctx.author}")

                # Fetch the filename using the Fetcher module
                filename = Fetcher(arg)

                # return error or link to file on gofile.io
                return ctx.send(filename)

            except Exception as e:
                # Log and send an error message
                Logger.error(f"Error: {str(e)}")
                await ctx.send(f"Error: {str(e)}")
