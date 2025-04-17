import os
import configparser
from configparser import ConfigParser

DEFAULT_CONFIG_PATH = "/var/opt/kaspersky/config.ini"


def read_config(config_path: str | None = None) -> ConfigParser:
    if config_path is None:

        config_path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    print(f"config path: {config_path}")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
