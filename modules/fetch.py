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

import os
import validators

from modules.downloader import Downloader
from modules.zipper import Zipper
from modules.uploader import Uploader
from modules.logger import Logger
from modules.name_gen import NameGenerator


class Fetch:
    def __init__(self):
        self.downloader = Downloader()
        self.name_gen = NameGenerator()
        self.zipper = Zipper()
        self.uploader = Uploader()
        self.temp_path = str(os.getenv("DISCORD_BOT_TEMP_FOLDER"))

    async def fetch(self, url: str, ctx):
        # start with giving random name for downloads

        try:
            # generate a random name
            await self.name_gen.generate_word(ctx, 10)
            Logger.info(f"Name gen successful name = {ctx.generated_name}")

            # download the stream
            await self.downloader.download(ctx, url)
            Logger.info(f"Download successful folder = {ctx.path_to_downloads}")  # type: ignore

            # zip the files
            await self.zipper.zipfile(ctx)
            Logger.info(f"Zip successful folder = {ctx.zip_file_name}")  # type: ignore

            # upload the zip file
            await self.upload(ctx)

        except Exception as e:
            # Log and send an error message with traceback
            Logger.error(f"Error: {str(e)}")
            await ctx.send(
                f"@{ctx.author.mention} something wen't wrong, blame assink!"
            )

    async def upload(self, ctx):
        try:
            await self.uploader.upload_file(ctx)
            Logger.info(f"Upload successful")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            await ctx.send(f"@{ctx.author} something wen't wrong! Error is logged.")
