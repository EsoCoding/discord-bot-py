import logging
import datetime
import inspect
from modules.bcolors import BColors


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.log = logging.getLogger("music-discord-bot")
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s - Line %(lineno)d"
            )
            file_handler = logging.FileHandler("music-dl-bot.log")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            cls._instance.log.addHandler(file_handler)
            logging.basicConfig(
                filename="music-dl-bot.log",
                filemode="w",
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - Line %(lineno)d",
                level=logging.DEBUG,
            )
        return cls._instance

    @staticmethod
    def info(message: str):
        module_name = inspect.stack()[1].filename.split("/")[-1].split(".")[0]
        print(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            + BColors.BOLD
            + BColors.OKBLUE
            + "INFO    "
            + BColors.ENDC
            + BColors.OKCYAN
            + f" {module_name} "
            + BColors.ENDC
            + message
        )
        Logger._instance.log.info(f"{message}\n")

    @staticmethod
    def error(message: str):
        module_name = inspect.stack()[1].filename.split("/")[-1].split(".")[0]
        print(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            + BColors.BOLD
            + BColors.FAIL
            + "ERROR    "
            + BColors.ENDC
            + BColors.OKCYAN
            + f" {module_name} "
            + BColors.ENDC
            + f" {inspect.stack()[1].filename} - Line {inspect.stack()[1].lineno} "
            + message
        )
        Logger._instance.log.error(f"{message}\n")
