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
        url = "https://store1.gofile.io/uploadFile"
        files = {"file": open(ctx.zip_file_name, "rb")}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "ok":
                ctx.go_file_link = str(data["data"]["downloadPage"])
                await ctx.send(f"{ctx.author} {ctx.go_file_link}")

        else:
            Logger.error("Upload failed")
            return
