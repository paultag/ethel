try:
    import configparser
except ImportError:
    import ConfigParser as configparser

CONFIG_BLOCK = "host"


def load(location="/etc/ethel.ini", block="host"):
    if block is None:
        block = CONFIG_BLOCK

    cfg = configparser.ConfigParser()
    cfg.read(location)
    return cfg[block]
