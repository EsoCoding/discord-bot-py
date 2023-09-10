import os
import zipfile
from modules.logger import Logger

class ZipFile:
    def __init__(self):
        pass

    def _zip_files(self, directory_path, zip_file_path):
        with zipfile.ZipFile(zip_file_path, "w") as zipFile:
            for file in os.listdir(directory_path):
                if file.endswith(".mp3"):
                    zipFile.write(os.path.join(directory_path, file), file)

    def _check_zip_success(self, zip_file_path):
        if os.path.exists(zip_file_path):
            return True
        else:
            Logger.error("Zip file does not exist!")
            raise FileNotFoundError("Zip file does not exist!")

    async def zipfile(self, ctx) -> None:
        directory_path = str(ctx.album_path)
        directory_name = str(ctx.album_name)
        zip_file_path = os.path.join(directory_path, directory_name + ".zip")

        Logger.info("Start zip...")

        try:
            self._zip_files(directory_path, zip_file_path)
        except Exception as e:
            Logger.error(f"Exception occurred during zip: {str(e)}")
            raise Exception("Something went wrong during zipping!")

        if self._check_zip_success(zip_file_path):
            Logger.info("Finished zipping file(s)")
            ctx.zip_file_name = zip_file_path
            return True