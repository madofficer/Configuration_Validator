import configparser
from configparser import ConfigParser


def read_config(config_path: str | None = None) -> ConfigParser:
    config_path = config_path if config_path is not None else "/var/opt/kaspersky/config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


if __name__ == "__main__":
    conf = read_config(r"E:\pets\KasperskyValidate\config\config.ini")
    print(type(conf))
    print(conf["General"])
