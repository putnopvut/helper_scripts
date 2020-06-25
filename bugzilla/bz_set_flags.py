#!/usr/bin/env python

# Set flags on a Bugzilla issue.
# Usage:
#  bz_set_flags.py <bug> <flag1> <value1> [<flag2> <value2> ...]
#
# This script will set the flags provided for the given <bug>.
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
from utilities import open_session, set_bz_flag


if __name__ == '__main__':
    parser = ArgumentParser(description="Set a flag on a bug")
    parser.add_argument('bug_number',
                        help="Bugzilla bug ID")
    parser.add_argument('flag_name',
                        help="Name of flag to set")
    parser.add_argument('flag_value',
                        help="Value of flag to set")
    args = parser.parse_args()

    session = open_session()

    set_bz_flag(session, args.bug_number, args.flag_name, args.flag_value)
