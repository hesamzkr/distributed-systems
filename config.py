import logging
import os

from dotenv import dotenv_values


class Config:
    SQL_URI = os.getenv("SQL_URI", "")

    def __init__(self):
        env_values = dotenv_values()
        logging.basicConfig(
            filename="app.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.__logger = logging.getLogger()
        self.__logger.info("Config initialized")
        self.SQL_URI = env_values.get("SQL_URI", "")


config = Config()
