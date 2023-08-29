#################################################################
# Created By:          Arjan Poortman
# Created Date:        2021-09-30
# ---------------------------------------------------------------
# Updated By:          Arjan Poortman
# Updated Date:        2021-10-01
# ---------------------------------------------------------------
# Update Info:       Added the Upload class
# ---------------------------------------------------------------
# Description:
# This module contains functions for uploading files.
# ---------------------------------------------------------------

import json
import os
import subprocess
import requests
from typing import List, Tuple
from modules.Logger import Logger


class Upload:
    def __init__(self, file_path: str):
        pass

    def upload_file(self, file_path: str) -> str:
        # use subproccess to upload the file to the gofile.io to
        # gofile using https://store1.gofile.io/uploadFile server using curl
        # if the upload is successful, return the url to the uploaded file
        # if the upload is not successful, return an error message
        json.response = subprocess.run(
            ["curl", "-F", f"file=@{file_path}", "https://store1.gofile.io/uploadFile"]
        ).stdout
        # check if the response is 200 add json response to the response variable
        # and pass it to the get_url function which will return the url to the uploaded file
        if json.response == 200:
            url = self.get_url(json.response)
            return url
        else:
            # if the upload was not successful, return an error message
            Logger.error(f"Could not upload file {file_path}")
            return "Could not upload file"

    def get_url(self, json_response: str) -> str:
        # fetch the url from the json response and return it
        return json_response["data"]["downloadPage"]
