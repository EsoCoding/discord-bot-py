import os
import glob
import subprocess
from modules.logger import Logger


class Downloader:
    """
    This class handles the downloading of the stream from the URL.
    """

    def __init__(self):
        """
        Initialize class variables.
        """
        pass

    @staticmethod
    def get_new_subdirectory(folder_path):
        """
        Get the first subdirectory in the given folder path.
        """
        subdirectories = glob.glob(os.path.join(folder_path, "*/"))
        if subdirectories:
            new_subdirectory = subdirectories[0].rstrip("/")
            return new_subdirectory, os.path.basename(new_subdirectory)
        else:
            return None, None

    async def download(self, ctx):
        """
        Download the stream from the URL and save it in the specified directory.
        """
        Logger.info("Start download...")
        try:
            # Use the 'rip' command line tool to download the stream.
            subprocess.run(
                [
                    "rip",
                    "url",
                    "--ignore-db",
                    "--directory=" + str(ctx.unique_path),
                    "--no-interaction",
                    str(ctx.url),
                ]
            )
        except Exception as e:
            Logger.error(f"Exception occurred during download: {str(e)}")
            raise ValueError("Something executing rip, download failed!")

        # Check if the new albums was actually downloaded by checking if the directory exists
        # and if it contains *.mp3 files.
        try:
            directory_path, directory_name = self.get_new_subdirectory(str(ctx.unique_path))
            if os.path.exists(directory_path) and os.path.isdir(directory_path):
                if glob.glob(os.path.join(directory_path, "*.mp3")):
                    # Set the name and path of the downloaded album in the context object.
                    Logger.info("Finished downloading file(s)")
                    Logger.info(f"folder:{directory_name} in path: {directory_path} do exist and contains mp3 files")
                    ctx.album_name = directory_name
                    ctx.album_path = directory_path
                    return True
        except Exception as e:
            Logger.error(f"Exception occurred during download: {str(e)}")
            raise ValueError("Something went wrong, new album does not exist!")