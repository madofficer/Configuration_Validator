import os
from dotenv import load_dotenv
import configparser
from configparser import ConfigParser

DEFAULT_CONFIG_PATH = "/var/opt/kaspersky/config.ini"


def read_config(config_path: str | None = None) -> ConfigParser:
    if config_path is None:
        load_dotenv()
        config_path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

