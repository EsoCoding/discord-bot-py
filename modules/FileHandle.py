# License: MIT License
# Description: This module contains functions for handling files.
# Contributors: Arjan Poortman (original author)
#

import os
from typing import Tuple
from urllib.parse import urlparse, parse_qs
from modules.Logger import Logger
from typing import List
from logging import Logger
import shutil


class FileHandle:
    def __init__(self):
        pass

    def parse_url(url):
        """
        Parse the given URL into its constituent parts.

        Parameters:
            url (str): The URL to be parsed.

        Returns:
            tuple: A tuple containing the parsed platform, content type, and content ID.
        """
        # Parse the URL into its constituent parts
        url_parts = urlparse(url)

        # Split the subdomain into its parts
        subdomain_parts = url_parts.netloc.split(".")

        # The first part of the subdomain represents the platform
        platform = subdomain_parts[0]

        # Split the URL path into its parts
        url_path_parts = url_parts.path.split("/")

        # The third part of the URL path represents the content ID
        content_id = url_path_parts[3]

        # The first part of the URL path represents the content type
        content_type = url_path_parts[1]

        # Return the parsed platform, content type, and content ID
        return platform, content_type, content_id

    def get_folder_and_file_names(url: str) -> Tuple[str, List[str]]:
        """
        Get the folder name and file names from the given URL.

        Parameters:
            url (str): The URL of the folder.

        Returns:
            Tuple[str, List[str]]: A tuple containing the folder name and a list of file names.
        """
        # iterate trough the temp folder and find the folder name and the file names
        for root, dirs, files in os.walk(str(os.getenv("DISCORD_BOT_TEMP_FOLDER"))):
            # if the folder name is not the temp folder name, return the folder name and the file names
            if root != str(os.getenv("DISCORD_BOT_TEMP_FOLDER")):
                return os.path.basename(root), files
            # if the folder name is the temp folder name, return the folder name and the file names
            # inside a list of strings
            else:
                return os.path.basename(root), files

    def remove_from_temp_files(author: str) -> bool:
        """
        Remove the temp directory and its contents.
        """

        # remove the temp folder and its contents
        # return true if the folder was removed, false otherwise
        if shutil.rmtree(
            str(os.join(str(os.getenv("DISCORD_BOT_TEMP_FOLDER")), author))
        ):
            Logger.info(f"Temp folder for {author} removed")
            return True
        else:
            Logger.error(f"Temp folder for {author} is not removed")
            return False

    def create_temporary_folder_for_user(author: str):
        """
        Create a temporary folder for the user.
        """
        # create a temporary folder for the user
        # return true if the folder was created, false otherwise
        status = os.mkdir(str(os.getenv("DISCORD_BOT_TEMP_FOLDER")) + "/" + author)

        if status:
            Logger.info("Temp folder created")
            return True
        else:
            Logger.error("Temp folder not created")
            return False
