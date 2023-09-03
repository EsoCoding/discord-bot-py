# this class handles the handling of downloading the stream from the url
# and return the url to music-bot.py class, so it can be returned to user
# who requested the album.
#
# It first initlizes the Download class which will download the album or
# to the temp folder.
#
# Then the zipper class will zip these files inside this
# folder and return the path of the zip file.
#
# Then at last the uploader class will upload the file to gofile.io
# and return the url from the gofile.io server to music-bot.py.

import asyncio
import os

import validators
from urllib.parse import urlparse

from modules.downloader import Downloader
from modules.zipper import Zipper
from modules.uploader import Uploader
from modules.logger import Logger
from modules.unique_path import UniquePath


class Fetch:
    def __init__(self):
        self.downloader = Downloader()
        self.unique_path = UniquePath()
        self.zipper = Zipper()
        self.uploader = Uploader()
        self.temp_path = str(os.getenv("DISCORD_BOT_TEMP_FOLDER"))

    async def fetch(self, url: str, ctx):
        # start with giving random name for downloads

        try:
            # check if url is valid
            await self.validate(ctx, url)

            # generate a path with a random folder name
            await self.generate(ctx)

            # download the stream
            await self.download(ctx)

            # zip the files
            await self.zipfile(ctx)

            # upload the zip file
            await self.upload(ctx)

        except Exception as e:
            # Log and send an error message with traceback
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"@{ctx.author} error occured while downloading! Error is logged."
            )
            exit()

    async def upload(self, ctx):
        try:
            await self.uploader.upload_file(ctx)
            Logger.info(f"Upload successful")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"{ctx.author} something wen't wrong with uploading! Error is logged."
            )
            exit()

    async def zipfile(self, ctx):
        try:
            await self.zipper.zipfile(ctx)
            Logger.info(f"Zip successful")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"{ctx.author} something wen't wrong with zipping! Error is logged."
            )
            exit()

    async def download(self, ctx):
        try:
            await self.downloader.download(ctx)
            Logger.info(f"Download successful")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"{ctx.author} something wen't wrong with downloading! Error is logged."
            )
            exit()

    async def generate(self, ctx):
        try:
            await self.unique_path.generate(ctx)
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"{ctx.author} something wen't wrong with generating path! Error is logged."
            )
            exit()

    async def validate(self, ctx, url: str):
        """
        Checks if the url is valid
        """
        try:
            if validators.url(url):
                ctx.url = url
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"{ctx.author} something wen't wrong with validating! Error is logged."
            )
            exit()
