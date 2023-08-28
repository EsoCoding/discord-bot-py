import subprocess
import os
import streamrip
from streamrip import utils

from modules.Logger import Logger
from modules.Zipper import Zipper

class Fetcher:
    def __init__(self, url: str):
        
        self.zipper = Zipper()

        # request = utils.gen_threadsafe_session()
        # header_keys = request.request(url=url, method="HEAD").headers.keys()
        # header_get = request.request(url=url, method="HEAD").headers.get("content-type")
        # header_split = header_get.split(";")[0]

        #rint(header_keys = {header_keys})
        #download = streamrip.downloadtools.DownloadStream(url=url, headers=header_get)
        #print(header_keys + {download.id})
        

    def get_file(self, url: str):
        
        self.logactions.info(f"About to start downloading {url}")         

        discord_bot_temp_folder = "--directory=" + str(os.getenv("DISCORD_BOT_TEMP_FOLDER"))
        quiet = "--quiet"
        if subprocess.run(["rip", "url", "--ignore-db", 'quiet', discord_bot_temp_folder, url]):
            self.Logger.info(f"Download complete")
            
    def zip_file(self):
        self.zipper.zip([os.path.join(str(os.getenv("DISCORD_BOT_TEMP_FOLDER")), "rip")], "rip.zip")        



