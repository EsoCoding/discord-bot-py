import os
import zipfile
from typing import List

class Zipper:
    def __init__(self):
        self.output_directory = str(os.getenv("DISCORD_BOT_TEMP_FOLDER"))

    def zip(self, files: List[str], archive_name: str = 'archive.zip') -> str:
        """
        Create a zip archive from a list of files.

        :param files: A list of file paths to include in the archive.
        :param archive_name: The name of the archive file.
        :return: The path of the created archive file.
        """
        archive_path = os.path.join(self.output_directory, archive_name)

        with zipfile.ZipFile(archive_path, 'w') as zipf:
            for file in files:
                zipf.write(file)

        return archive_path
