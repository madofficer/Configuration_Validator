import os
# uncomment if you want to use .env file
# from dotenv import load_dotenv
import configparser
from configparser import ConfigParser

DEFAULT_CONFIG_PATH = "/var/opt/kaspersky/config.ini"


def read_config(config_path: str | None = None) -> ConfigParser:
    if config_path is None:
        # uncomment if you want to use .env file
        # load_dotenv()
        config_path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)
        # config_path = str(Path(config_path).resolve())

    print(f"config path: {config_path}")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
