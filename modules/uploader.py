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

    async def upload_file(self, ctx) -> None:
        gofile_alive_url = "https://api.gofile.io/getServer"

        response = requests.get(gofile_alive_url)

        if response.status_code == 200:
            Logger.info("Connection with gofile.io established")

            Logger.info("trying to Uploading file to gofile.io")

            upload_url = "https://store2.gofile.io/uploadFile"
            files = {"file": open(ctx.zip_file_name, "rb")}
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                data = response.json()
                if data["status"] == "ok":
                    ctx.author.mention.value = str(data["data"]["downloadPage"])
                    ctx.go_file_link = str(data["data"]["downloadPage"])
                    await ctx.send(f"{ctx.author}")
                    return True
            else:
                Logger.error(
                    "Upload failed, response code: " + str(response.status_code)
                )
                return False
        else:
            Logger.error("Connection issues with gofile.io")
            return False
