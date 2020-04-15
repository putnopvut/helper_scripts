import configparser
from pathlib import Path


def get_api_key(domain):
    config = configparser.ConfigParser()
    paths = [
        Path(Path.home(), '.config', 'bugzillarc'),
        Path(Path.home(), '.bugzillarc'),
        Path('.bugzillarc'),
    ]

    config.read(paths)
    return config[domain]['api_key']
