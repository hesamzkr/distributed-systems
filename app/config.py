import logging
import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        logging.basicConfig(
            filename="app.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.__logger = logging.getLogger()
        self.__logger.info("Config initialized")
        self.SQL_URI = os.getenv("SQL_URI", "")
        self.SQL_URI_2 = os.getenv("SQL_URI_2", "")
        self.SERVICE_URL = os.getenv("SERVICE_URL")
        self.PUBLIC_URL = os.getenv("PUBLIC_URL")


config = Config()
