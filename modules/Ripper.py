import subprocess
import os
import streamrip

from streamrip import *

from modules.Logger import Logger
from modules.Zipper import Zipper

class Ripper:
    def __init__(self, url: str):
        self.zipper = Zipper(__name__)
        self.logger = Logger(__name__)

        self.clients = streamrip.downloadtools.DownloadStream(url)

    def get_file(self, url_link: str):
        
        self.Logger.info(f"About to start downloading {url_link}", __name__)         

        discord_bot_temp_folder = "--directory=" + str(os.getenv("DISCORD_BOT_TEMP_FOLDER"))
        stdout = subprocess.run(["rip", "url", "--ignore-db", discord_bot_temp_folder, url_link]) 
        
        if stdout == 0:
            self.Logger.info(f"Download complete {stdout}", __name__)
        else:
            self.Logger.error(f"Download failed {stdout}", __name__)

        self.zipper.zip([os.path.join(str(os.getenv("DISCORD_BOT_TEMP_FOLDER")), "rip")], "rip.zip")        

        return True