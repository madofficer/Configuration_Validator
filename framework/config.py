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


if __name__ == "__main__":
    print(os.getenv("CONFIG_PATH"))
    conf = read_config()
    print(type(conf))
    print(conf["General"])
