from typing import Optional

import os
import sys
import pathlib

import discord
from discord import Intents
from discord.ext import commands

# Import the logger, URLValidator, UniquePath,
from modules.validate import Validation
from modules.unique_path import UniquePath
from modules.downloader import Downloader
from modules.zipfile import ZipFile
from modules.uploader import Uploader
from modules.logger import Logger

# path lib set rootdir
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=Intents.all())
        self.commands = commands.Bot(command_prefix=os.environ.get("DISCORD_BOT_PREFIX"), intents=Intents.all())
        self.validation = Validation()
        self.unique_path = UniquePath()
        self.downloader = Downloader()
        self.zipfile = ZipFile()
        self.uploader = Uploader()
        
        

    def start(self):
        

        @self.commands.event
        async def on_ready():
            Logger.info(f"You are now logged in as: {self.commands.user}")
                    
        @self.commands.command(name="download", help="Download a file from a URL")
        async def download(ctx, url: str):
            # validate the url
            if await self.validation.validate(ctx, url):
                ctx.send(f"{ctx.author.mention} processing request, i'll send you a message when your haul has arrived!")
                # generate a path with a random folder name
                await self.unique_path.generate(ctx)
                # download the files
                await self.downloader.download(ctx)
                # zip the files
                await self.zipfile.zipfile(ctx)
                # upload the files
                if await self.uploader.upload_file(ctx):
                    
                    user = await self.commands.fetch_user(int(ctx.author.id))
                    await user.send(f"{ctx.author.mention} your haul has arrived, you can find it here: {ctx.go_file_link}")
                    
                    Logger.info(f"sended message to {ctx.author.name} with download link: {ctx.go_file_link}")
                    
                # delete the temp folder
                if await self.unique_path.delete(ctx):
                    Logger.info("Deleted temp folder")

            else:
                # Log the error
                Logger.error("Invalid URL")
                await ctx.send("Invalid URL")

        
        @self.commands.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"This command is on cooldown, please retry in {error.retry_after:.2f}s.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Missing required argument: {error.param.name}")
            elif isinstance(error, commands.BadArgument):   
                await ctx.send(f"Bad argument: {error}")
            elif isinstance(error, commands.MemberNotFound):   
                await ctx.send(f"Could not find member by given string")
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(f"Missing permissions: {error}")
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.send(f"Bot missing permissions: {error}")
            elif isinstance(error, commands.CommandNotFound):
                await ctx.send(f"Command not found: {error}")
        
        self.commands.run(os.environ.get("DISCORD_BOT_TOKEN"))
        
        