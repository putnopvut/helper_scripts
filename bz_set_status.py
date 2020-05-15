#!/usr/bin/env python

# Set status on a Bugzilla issue.
# Usage:
#  bz_set_status.py <bug> <status>
#
# This script will set <bug>'s status to <status>.
# Acceptable status values are:
# * NEW
# * ASSIGNED
# * POST
# * MODIFIED
# * ON_QA
# * VERIFIED
# * RELEASE_PENDING
# * CLOSED
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


import sys
from utilities import open_session, REST_URL


def set_bz_status(session, bugno, status):
    print(f"Setting the status on {bugno} to {status}:")

    r = session.put(f'{REST_URL}/rest/bug/{bugno}', json={'status': status})

    r.raise_for_status()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please include BZ bug number and status.")
        sys.exit(1)

    bugno = sys.argv[1]
    status = sys.argv[2]

    session = open_session()

    set_bz_status(session, bugno, status)
