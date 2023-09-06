import os
import subprocess
import json
from urllib import request
import certifi
from io import BytesIO
from modules.logger import Logger
from inspect import currentframe
import requests


class Uploader:
    def __init__(self):
        self.buffer = BytesIO()

    def get_gofile_server(self):
        gofile_alive_url = "https://api.gofile.io/getServer"
        response = requests.get(gofile_alive_url).json()
        if response["status"] == "ok":
            Logger.info("Connection with gofile.io established")
            return response['data']['server']
        else:
            Logger.error("Connection with gofile.io failed")
            raise ConnectionError("Connection with gofile.io failed")

    def upload_file_to_gofile(self, server, file_path):
        upload_url = f"https://{server}.gofile.io/uploadFile"
        Logger.info(f"Upload url: {upload_url}")
        with open(file_path, "rb") as file:
            response = requests.post(upload_url, files={"file": file})
        return response

    def handle_upload_response(self, response):
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "ok":
                Logger.info("Upload successful")
                return str(data["data"]["downloadPage"])
        Logger.error(
            "Upload failed, response code: " + str(response.status_code)
        )
        raise ValueError("Upload failed, response code: " + str(response.status_code))

    async def upload_file(self, ctx) -> None:
        try:
            Logger.info("trying to Uploading file to gofile.io")
            server = self.get_gofile_server()
            response = self.upload_file_to_gofile(server, ctx.zip_file_name)
            ctx.go_file_link = self.handle_upload_response(response)
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            raise ValueError(f"Upload failed, error {str(e)}")
