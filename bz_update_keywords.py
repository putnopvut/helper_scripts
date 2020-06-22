#!/usr/bin/env python

# Update keywords on a Bugzilla issue.
# Usage:
#  bz_update_keywords.py --action <bug> <keyword>
#
# This script will update the keyword provided for the given <bug>.
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
from utilities import open_session, REST_URL


def update_bz_keywords(session, bugno, keywords, action):
    print(f"{action} keywords {keywords} on {bugno}")

    params = {}
    params[action] = keywords
    r = session.put(f'{REST_URL}/bug/{bugno}', json={'keywords': params})

    r.raise_for_status()


if __name__ == '__main__':
    parser = ArgumentParser(description="Update keywords")
    parser.add_argument('bugno', help="Bugzilla bug number")
    parser.add_argument('keywords', nargs='+',
                        help='Keywords to update')
    parser.add_argument('--action', choices=['add', 'remove', 'set'],
                        default='add',
                        help='Action to take with keywords')

    args = parser.parse_args()

    session = open_session()

    update_bz_keywords(session, args.bugno, args.keywords, args.action)
