# This class represents a Zipper object that is responsible for zipping the mp3 files in the temp folder
# which are downloaded by streamrip.

import os
import subprocess
import glob

from modules.logger import Logger


class Zipper:
    def __init__(self):
        pass

    import glob

    def get_new_subdirectory_path(self, folder_path):
        subdirectories = glob.glob(folder_path + "/*/")
        if subdirectories:
            new_subdirectory = subdirectories[0].rstrip("/")
            return new_subdirectory
        else:
            return None

    def get_new_subdirectory_name(self, folder_path):
        subdirectories = glob.glob(folder_path + "/*/")
        if subdirectories:
            new_subdirectory = os.path.basename(subdirectories[0].rstrip("/"))
            return new_subdirectory
        else:
            return None

    async def zipfile(self, ctx) -> None:
        # Set the path of the zip file.

        path = str(ctx.path_to_downloads)

        directory_path = self.get_new_subdirectory_path(path)

        directory_name = self.get_new_subdirectory_name(path)

        print(directory_name)
        # get new subfolder name from path

        # Zip the files in the temp folder.
        Logger.info("Start zip...")

        try:
            # Use the 'rip' command line tool to download the stream.
            output = subprocess.run(
                [
                    "zip",
                    "-r",
                    path + "/" + directory_name + ".zip",
                    directory_path,
                ]
            )
        except Exception as e:
            # Handle any exception that occurs during the download.
            Logger.error(f"Exception occurred during zip: {str(e)}")
            return

        # Check if the download was successful.
        if output.returncode == 0:
            # get name + path and pass it to ctx
            ctx.zip_file_name = os.path.join(
                ctx.path_to_downloads, directory_name + ".zip"
            )
