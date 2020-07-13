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


def update_bz(session, bugno, json):
    r = session.put(f'{REST_URL}/bug/{bugno}', json=json)
    r.raise_for_status()


def set_bz_flags(session, bugno, flag_dict):
    flags = [{'name': k, 'status': v} for k, v in flag_dict.items()]

    print(f"Setting the following flags on {bugno}:")
    for f in flags:
        print(f"  {f['name']}: {f['status']}")

    update_bz(session, bugno, {'flags': flags})


def update_bz_keywords(session, bugno, keywords, action):
    print(f"{action} keywords {keywords} on {bugno}")

    update_bz(session, bugno, {action: keywords})


def set_bz_flag(session, bugno, flag_name, flag_val):
    set_bz_flags(session, bugno, {flag_name: flag_val})


def search_bz(session, params):
    r = session.get(f'{REST_URL}/bug', params=params)
    r.raise_for_status()
    return r.json()['bugs']


def get_bz_bugs(session, bugs):
    bug_str = ','.join(bugs)
    return search_bz(session, {'id', bug_str})


def get_bz_bug(session, bugno):
    r = session.get(f'{REST_URL}/bug/{bugno}')
    r.raise_for_status()
    return r.json()['bugs'][0]
