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
        self.commands.add_listener(self.on_ready)

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
                    await self.message_user(ctx, user, f"Here is your haul {ctx.go_file_link}")
                    
                    Logger.info(f"sended message to {ctx.author.name} with download link: {ctx.go_file_link}")
                    
                # delete the temp folder
                if await self.unique_path.delete(ctx):
                    Logger.info("Deleted temp folder")

            else:
                # Log the error
                Logger.error("Invalid URL")
                await ctx.send("Invalid URL")

        self.commands.run(os.environ.get("DISCORD_BOT_TOKEN"))

    async def message_user(self, context, user: discord.User, message):
        await user.send(message)


    async def on_ready(self):
        Logger.info(f"You are now logged in as: {self.commands.user}")

