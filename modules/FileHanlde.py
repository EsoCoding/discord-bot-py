## utils.py
import os
from typing import Tuple
from urllib.parse import urlparse, parse_qs
from modules.Logger import LogActions
from typing import List


class FileHandle:
    def __init__(self):
        pass
        self.logger = LogActions(__name__)

    def parse_url(url: str) -> tuple[str, str, str]:
        """
        Parse a URL to extract the platform, type of content, and content ID.

        :param url: The URL to parse.
        :return: A tuple containing the platform, type of content, and content ID.
        """
    def parse_url(url):
        # Parse the URL into its constituent parts
        url_parts = urlparse(url)
    
        # Split the subdomain into its parts
        subdomain_parts = url_parts.netloc.split('.')

        # The first part of the subdomain represents the platform
        platform = subdomain_parts[0]

        # Split the URL path into its parts
        url_path_parts = url_parts.path.split('/')

        # The third part of the URL path represents the content ID
        content_id = url_path_parts[3]

        # The first part of the URL path represents the content type
        content_type = url_path_parts[1]

        # Return the parsed platform, content type, and content ID
        return platform, content_type, content_id


    def get_file_paths(directory: str) -> List[str]:
        """
        Get the paths of all files in a directory.

        :param directory: The directory to search.
        :return: A list containing the paths of all files in the directory.
        """
        file_paths = []
        
    def get_file_paths(directory):
        """
        Recursively walks through the given directory and returns a list of all file paths.
        """
        # Create an empty list to store the file paths
        file_paths = []

        # Iterate over each directory and its subdirectories in the specified directory
        for root, _, files in os.walk(directory):
            # Iterate over each file in the current directory
            for filename in files:
                # Combine the root path and the file name to get the full file path
                file_paths.append(os.path.join(root, filename))

        # Return the list of file paths
        return file_paths