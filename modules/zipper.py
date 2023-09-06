import os
import subprocess
import glob
import zipfile
import string
from modules.logger import Logger


class Zipper:
    def __init__(self):
        pass

    def get_new_subdirectory_path(self, folder_path):
        subdirectories = glob.glob(os.path.join(folder_path, "*/"))
        if subdirectories:
            new_subdirectory = subdirectories[0].rstrip("/")
            return new_subdirectory
        else:
            return None

    def get_new_subdirectory_name(self, folder_path):
        subdirectories = glob.glob(os.path.join(folder_path, "*/"))
        if subdirectories:
            new_subdirectory = os.path.basename(subdirectories[0].rstrip("/"))
            return new_subdirectory
        else:
            return None

    async def zipfile(self, ctx) -> None:
        # Set the path of the zip file.
        path = str(ctx.unique_path)

        directory_path = self.get_new_subdirectory_path(path)

        directory_name = self.get_new_subdirectory_name(path)

        # Zip the files in the temp folder.
        Logger.info("Start zip...")

        try:
            # Use the 'zip' command line tool to create the zip file.
            zip_file_path = os.path.join(path, directory_name + ".zip")
            with zipfile.ZipFile(zip_file_path, "w") as zipFile:
                for file in os.listdir(directory_path):
                    if file.endswith(".mp3"):
                        zipFile.write(os.path.join(directory_path, file), file)
        except Exception as e:
            # Handle any exception that occurs during the zip process.
            Logger.error(f"Exception occurred during zip: {str(e)}")
            raise ("Somethign wen't wrong during zipping!")

        # Check if the zip process was successful.
        try:
            if os.path.exists(os.path.exists(zip_file_path)):
                # Set the name and path of the zip file in the context object.
                Logger.info("Finished zipping file(s)")
                ctx.zip_file_name = zip_file_path
                return True
        except Exception as e:
            # Handle any exception that occurs during the zip process.
            Logger.error(f"Zip file does not exist!")
            raise
