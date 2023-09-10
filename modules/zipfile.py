import os
import zipfile
from modules.logger import Logger

class ZipFile:
    def __init__(self):
        pass

    def _zip_files(self, directory_path, zip_file_path):
        """
        Zip the files in the specified directory and save them to a new zip file.

        Args:
            directory_path (str): The path of the directory containing the files to be zipped.
            zip_file_path (str): The path of the new zip file to be created.

        Returns:
            None
        """
        # Create a new zip file at the specified path
        with zipfile.ZipFile(zip_file_path, "w") as zipFile:
            # Iterate over each file in the directory
            for file in os.listdir(directory_path):
                # Check if the file ends with ".mp3"
                if file.endswith(".mp3"):
                    # Add the file to the zip file with the same name
                    zipFile.write(os.path.join(directory_path, file), file)

    def _check_zip_success(self, zip_file_path):
        """
        Check if the zip file exists.

        Args:
            zip_file_path (str): The path to the zip file.

        Returns:
            bool: True if the zip file exists, False otherwise.

        Raises:
            FileNotFoundError: If the zip file does not exist.
        """
        # Check if the zip file exists
        if os.path.exists(zip_file_path):
            return True
        else:
            # Log an error message
            Logger.error("Zip file does not exist!")
            # Raise a FileNotFoundError exception
            raise FileNotFoundError("Zip file does not exist!")

    async def zipfile(self, ctx) -> None:
        # Get the directory path and name from the context
        directory_path = str(ctx.album_path)
        directory_name = str(ctx.album_name)
        
        # Create the path for the zip file
        zip_file_path = os.path.join(directory_path, directory_name + ".zip")

        # Log that the zip process has started
        Logger.info("Start zip...")

        try:
            # Zip the files in the directory
            self._zip_files(directory_path, zip_file_path)
        except Exception as e:
            # Log any exceptions that occur during the zip process
            Logger.error(f"Exception occurred during zip: {str(e)}")
            raise Exception("Something went wrong during zipping!")

        # Check if the zip process was successful
        if self._check_zip_success(zip_file_path):
            # Log that the zip process has finished and update the context with the zip file name
            Logger.info("Finished zipping file(s)")
            ctx.zip_file_name = zip_file_path
            return True
