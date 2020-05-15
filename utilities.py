import configparser
import requests
from pathlib import Path

DOMAIN = 'bugzilla.redhat.com'
REST_URL = f'https://{DOMAIN}/rest'


def get_api_key():
    config = configparser.ConfigParser()
    paths = [
        Path(Path.home(), '.config', 'bugzillarc'),
        Path(Path.home(), '.bugzillarc'),
        Path('.bugzillarc'),
    ]

    config.read(paths)
    return config[DOMAIN]['api_key']


def open_session():
    session = requests.Session()
    session.params.update({'api_key': get_api_key()})
    return session
