# Description: This class handles the fetching of the stream from the url
# and returns the folder and file names and create a archtve
# with the name of the folder
# Desc: Fetches the stream from the url and returns the file path
# Returns: str

import subprocess
import os
from turtle import down
import streamrip
from streamrip import utils
from .FileHandle import FileHandle

from modules.Logger import Logger
from modules.Zipper import Zipper
from modules.Upload import Upload


class Fetcher:
    def __init__(self):
        # create instance for
        self.zipper = Zipper()
        self.file_handle = FileHandle()

    def create_upload_file_from_stream_rip(self, url: str, author: str) -> str:
        #
        # log that download preocess started
        Logger.info(f"Downloading process started {url}")

        # first to be sure streamrip runs smoothly, remove if any at all exist
        # previous files from the temp folder.
        if self.file_handle.remove_from_temp_files(
            str(os.getenv("DISCORD_BOT_TEMP_FOLDER")) + "/" + author
        ):
            # if the files were removed, log it
            Logger.info(f"Removed previous files from {author} in temp folder")

        # Download the stream from the url and return the file path
        quiet = "--quiet"
        directory = (
            "--directory=" + str(os.getenv("DISCORD_BOT_TEMP_FOLDER")) + "/" + author
        )
        if subprocess.run(
            [
                "rip",
                "url",
                "--quiet",
                "--ignore-db",
                directory,
                quiet,
                str(os.getenv("DISCORD_BOT_TEMP_FOLDER")),
                url,
            ]
        ):
            # Find the album directory and filenames, and return them
            # using the get_folder_and_file_names function
            folder_name, file_names = FileHandle.get_folder_and_file_names(url)

            # zip the ripstream folder and files and name it after the folder_name variable
            # upload files go gofile.io and return the link

            Logger.info(f"Uploading now {folder_name}.zip")
            # Pass archive path to upload function, and return the gohost.io url
            # to which the zip_file was uploaded
            download_link = Upload().upload_file(
                self.zipper.zip(archive_name=folder_name, files=file_names)
            )

            if download_link:
                # if the download link is not empty, return the download link
                # Now we can remove the temp directory and its contents
                FileHandle.remove_temp_directory()

                return download_link
            else:
                # if the download link is empty, return an error message
                Logger.error(f"Could not upload {folder_name}.zip")
                return "Could not upload file"

        else:
            # if subprocess was not successful, return error message and log it.
            Logger.error(f"Subprocessed failed and could not download {url}")
