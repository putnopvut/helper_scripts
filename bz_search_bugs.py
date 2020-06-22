#!/usr/bin/env python

# Search for BZ issues and return their bug numbers.
# Usage:
#   bz_search_bugs.py --summary="keywords"
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
from utilities import open_session, search_bz

if __name__ == '__main__':
    search_fields = [
        "assigned_to",
        "component",
        "creator",
        "platform",
        "priority",
        "product",
        "qa_contact",
        "resolution",
        "severity",
        "status",
        "summary",
        "tags",
        "target_milestone",
        "url",
        "version",
        "whiteboard",
    ]
    parser = ArgumentParser(description="Search for bugs")
    for field in search_fields:
        parser.add_argument(f'--{field}',
                            help=f"Bugzilla '{field}' field")

    args = parser.parse_args()
    params = {}
    for field in search_fields:
        try:
            setattr(args, field, getattr(args, field).split(','))
            params[field] = getattr(args, field)
        except AttributeError:
            # Command line didn't set one of the fields. Not a problem.
            pass

    session = open_session()
    bugs = search_bz(session, params)
    for bug in bugs:
        print(bug['id'])
