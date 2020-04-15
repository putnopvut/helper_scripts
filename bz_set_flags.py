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


import sys
import requests
import utilities

if len(sys.argv) < 4:
    print("Please include BZ bug number, plus at least one flag and value.")
    sys.exit(1)

bugno = sys.argv[1]
flag_args = sys.argv[2:]

if len(flag_args) % 2 != 0:
    print(f"All flags must have values provided")
    sys.exit(1)

domain = 'bugzilla.redhat.com'
try:
    api_key = utilities.get_api_key(domain)
except Exception:
    print("No configured api_key found")
    sys.exit(1)

s = requests.Session()
s.headers.update({'api_key': api_key})

it = iter(flag_args)
flags = [{'name': flag, 'status': next(it)} for flag in it]

print(f"Setting the following flags on {bugno}:")
for f in flags:
    print(f"  {f['name']}: {f['status']}")

r = s.put(f'https://{domain}/rest/bug/{bugno}', json={'flags': flags})

r.raise_for_status()
