from calendar import c
import subprocess
import os
from modules.logger import Logger


class Downloader:
    # This class handles the downloading of the stream from the URL.

    def __init__(self):
        # Initialize class variables
        pass

    async def download(self, ctx, url):
        self.path = (
            str(os.getenv("DISCORD_BOT_TEMP_FOLDER")) + "/" + str(ctx.generated_name)
        )

        # Download the stream from the URL and save it in the specified directory.
        Logger.info("Start download...")
        try:
            # Use the 'rip' command line tool to download the stream.
            output = subprocess.run(
                [
                    "rip",
                    "url",
                    "--ignore-db",
                    "--directory=" + str(self.path),
                    "--quiet",
                    "--no-interaction",
                    url,
                ]
            )
        except Exception as e:
            # Handle any exception that occurs during the download.
            Logger.error(f"Exception occurred during download: {str(e)}")
            return

        # Check if the download was successful.
        if output.returncode == 0:
            # Set the 'folder_name' attribute of the 'ctx' object to the name of the newly created folder.
            ctx.path_to_downloads = self.path
