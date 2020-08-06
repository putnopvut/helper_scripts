#!/usr/bin/env python

# Retrieve attachments from a Bugzilla issue.
# Usage:
#   bz_get_attachments.py <bug_number>
#
# This script retrieves the attachments for <bug_number>.
#
# Attachments are saved to $HOME/bugzilla/<bug_number>/
# If the directory does not exist, it will be created.
#
# This script uses a bugzilla API key for authentication. The
# API key should be stored in a config file like so:
#
# [bugzilla.redhat.com]
# api_key = <key>
#
# You can generate an API key at
# https://bugzilla.redhat.com/userprefs.cgi?tab=apikey
#
# The script searches the following files for configuration
#   ~/.config/bugzillarc
#   ~/.bugzillarc
#   $PWD/.bugzillarc
#
# The files are searched in that order.


from argparse import ArgumentParser
import os
from pathlib import Path
import base64
from utilities import open_session, REST_URL


def get_bz_attachments(session, bugno):
    r = session.get(f'{REST_URL}/bug/{bugno}/attachment')

    r.raise_for_status()
    return r.json()['bugs'][bugno]


def write_bz_attachments(attachments, path):
    print(f"Creating directory {path} if it does not already exist")
    os.makedirs(path, exist_ok=True)

    for att in attachments:
        write_path = Path(path, Path(att['file_name']))
        with open(write_path, 'wb') as att_file:
            print(f'Writing {att_file.name}')
            att_file.write(base64.b64decode(att['data']))


if __name__ == '__main__':
    parser = ArgumentParser(description="Download and save "
                                        "Bugzilla attachments")
    parser.add_argument("bugno", help="Bugzilla bug ID")
    args = parser.parse_args()

    session = open_session()
    att = get_bz_attachments(session, args.bugno)
    write_bz_attachments(att, Path(Path.home(), Path('bugzilla'),
                         Path(args.bugno)))
