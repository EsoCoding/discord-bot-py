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
from modules.validate import URLValidator
from modules.unique_path import UniquePath
from modules.downloader import Downloader
from modules.zipfile import ZipFile
from modules.uploader import Uploader

# This class represents the MusicBot
class MusicBot:
    def __init__(self):
        self.client = commands.Bot(
            command_prefix=os.getenv("DISCORD_BOT_PREFIX"), intents=Intents.all()
        )
        self.unique_path = UniquePath()
        self.validation = URLValidator()
        self.downloader = Downloader()
        self.zipfile    = ZipFile()
        self.uploader   = Uploader()
        self.client.add_listener(self.on_ready)
        self.client.command()(self.dl)
    
    def on_ready(self, ctx):
        Logger.info(f"Logged in as {self.client.user}")

    @commands.cooldown(1, 20, commands.BucketType.channel)
    async def dl(self, ctx, arg):
        # validate the url
        if await self.validation.validate(ctx, arg):
            # generate a path with a random folder name
            generate_status = await self.unique_path.generate(ctx)

            download_status = await self.downloader.download(ctx)

            zipfile_status  = await self.zipfile.zipfile(ctx)

            if await self.uploader.upload_file(ctx):
                await ctx.send(f"{ctx.author.mention} ")

                channel_id = int(os.environ.get("DISCORD_BOT_CHANNEL_ID"))
                channel = self.client.get_channel(channel_id)
                
                if channel is None:
                    Logger.error(f"Error: Could not find channel with ID {channel_id}")
                else:
                    await channel.send(f"{ctx.author.mention} your present is ready: {ctx.go_file_link}")     
                    Logger.info(f"sended message to channel to {ctx.author.mention} with upload link: {ctx.go_file_link}")

            if await self.unique_path.delete(ctx):
                Logger.info("Deleted temp folder")

        else:
            # Log the error
            Logger.error("Invalid URL")
            await ctx.send("Invalid URL")
    
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