# Import the os and discord libraries
from imaplib import Commands
import os
from venv import logger
import discord

# Import discord class and Intents class
# from the discord library
from discord import Intents
from discord.ext import commands

from modules.logger import Logger
from modules.fetch import Fetch
from modules.validate import URLValidator
from modules.unique_path import UniquePath
from modules.downloader import Downloader


# This class represents the MusicBot
class MusicBot(commands.Bot):
    # This is the constructor of the MusicBot class
    def __init__(self):
        pass
    async def on_ready(self):
        # Log that the bot is logged in and print it to the console
        Logger.info(f"Bot is now logged in as {self.client.user}")
        # set status of the bot to online
        await self.client.change_presence(
            status=discord.Status.online, activity=None
        )
    async def on_message(self, message):
        # Process the message
        await self.client.process_commands(message)

        # Event handler for when the bot receives a command error  # event decorator/wrapper
    async def on_command_error(self, ctx, error):
        # Log the error and send an error message
        Logger.error(f"Error: {str(error)}")
        await ctx.send(f"Error: {str(error)}")

    async def validate_url(self, ctx, arg):
        if await self.validation.validate(ctx, arg):
            logger.info(f"Valid URL {arg}")
            return True
        else:
            await ctx.on_command_error(self, ctx, f"{arg} is an invalid URL.")
            return False
        
    async def generate_path(self, ctx):
        if await self.unique_path.generate():
            return True
        else:
            return False
        
    async def download(ctx):
        if await ctx.generate_path(ctx):
            return True
        else:
            return False

        
        # Command handler for the "dt" command

    @commands.cooldown(1, 20, commands.BucketType.channel)
    async def dl(self, ctx, arg):
        # validate the url
        if await self.validate_url(ctx, arg):
            # generate a path with a random folder name
            if await self.generate_path(ctx):

                await self.download(ctx)

        # cooldown error handler
        @dl.error
        async def dl_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(
                    f"{error.retry_after:.2f}s"
                )
            else:
                raise error
  
        