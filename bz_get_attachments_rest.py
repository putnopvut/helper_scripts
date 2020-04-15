#!/usr/bin/env python

# Retrieve attachments from a Bugzilla issue.
# Usage:
#   bz_get_attachments.py <bug_number>
#
# This script will prompt the user for login
# credentials for redhat.bugzilla.com, and then will
# retrieve the attachments for <bug_number>.
#
# Attachments are saved to $HOME/bugzilla/<bug_number>/
# If the directory does not exist, it will be created.
#
# The difference between this and bz_get_attachments.py
# is that this uses the REST API instead of python-bugzilla,
# which uses xmlrpc.

import requests
import sys
import os
from pathlib import Path
import base64
import configparser

if len(sys.argv) < 2:
    print("Please include a BZ bug number")
    sys.exit(1)

bugno = sys.argv[1]

config = configparser.ConfigParser()
paths = [
    Path(Path.home(), '.config', 'bugzillarc'),
    Path(Path.home(), '.bugzillarc'),
    Path('.bugzillarc'),
]

config.read(paths)
domain = 'bugzilla.redhat.com'

try:
    api_key = config[domain]['api_key']
except KeyError:
    print("No configured api_key found")
    sys.exit(1)

s = requests.Session()
s.headers.update({'api_key': api_key})

url = f'https://{domain}'

r = s.get(f'{url}/rest/bug/{bugno}/attachment')

if r.status_code != 200:
    print("Failed to retrieve attachments")
    sys.exit(1)

path = Path(Path.home(), Path('bugzilla'), Path(bugno))

print(f"Creating directory {path} if it does not already exist")
os.makedirs(path, exist_ok=True)

for att in r.json()['bugs'][bugno]:
    write_path = Path(path, Path(att['file_name']))
    with open(write_path, 'wb') as fi:
        print(f'Writing {fi.name}')
        fi.write(base64.b64decode(att['data']))
