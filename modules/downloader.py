from calendar import c
import subprocess
import os
from modules.logger import Logger


class Downloader:
    # This class handles the downloading of the stream from the URL.

    def __init__(self):
        # Initialize class variables
        pass

    async def download(self, ctx):
        # Download the stream from the URL and save it in the specified directory.
        Logger.info("Start download...")
        try:
            # Use the 'rip' command line tool to download the stream.
            output = subprocess.run(
                [
                    "rip",
                    "url",
                    "--ignore-db",
                    "--directory=" + str(ctx.unique_path),
                    "--quiet",
                    "--no-interaction",
                    str(ctx.url),
                ]
            )
        except Exception as e:
            # Handle any exception that occurs during the download.
            Logger.error(f"Exception occurred during download: {str(e)}")
            return

        # Check if the download was successful.
        if output.returncode == 0:
            # Set the 'folder_name' attribute of the 'ctx' object to the name of the newly created folder.
            return
