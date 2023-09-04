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

        response = requests.get(gofile_alive_url).json()

        print(response)

        if response["status"] == "ok":
            Logger.info("Connection with gofile.io established")

            Logger.info("trying to Uploading file to gofile.io")

            upload_url = f"https://{response['data']['server']}.gofile.io/uploadFile"
            Logger.info(f"Upload url: {upload_url}")

            try:
                files = {"file": open(ctx.zip_file_name, "rb")}
                response = requests.post(upload_url, files=files)

                if response.status_code == 200:
                    data = response.json()
                    if data["status"] == "ok":
                        Logger.info("Upload successful")
                        ctx.go_file_link = str(data["data"]["downloadPage"])
                        await ctx.send(f"{ctx.author}")
                        return True
                else:
                    Logger.error(
                        "Upload failed, response code: " + str(response.status_code)
                    )
                    return False

            except Exception as e:
                Logger.error(f"Error: {str(e)}")
                return False
