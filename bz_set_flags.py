#!/usr/bin/env python

# Set flags on a Bugzilla issue.
# Usage:
#  bz_set_flags.py <bug> <flag1> <value1> [<flag2> <value2> ...]
#
# This script will prompt the user for login
# credentials for redhat.bugzilla.com and then
# set the flags provided for the given <bug>.

import bugzilla
import sys

URL = "bugzilla.redhat.com"
bzapi = bugzilla.Bugzilla(URL)

if len(sys.argv) < 4:
    print("Please include BZ bug number, plus at least one flag and value.")
    sys.exit(1)

if len(sys.argv[2:]) % 2 != 0:
    print(f"All flags must have values provided")
    sys.exit(1)

bugno = sys.argv[1]

it = iter(sys.argv[2:])
flags = {flag: next(it) for flag in it}

if not bzapi.logged_in:
    bzapi.interactive_login()

print(f"Retrieving bug {bugno}")
try:
    bug = bzapi.getbug(bugno)
except Exception:
    print(f"Failed to retrieve bug {bugno}. Exiting")
    sys.exit(1)

print(f"Setting the following flags on {bugno}:")
for k, v in flags.items():
    print(f"  {k} = '{v}'")
bug.updateflags(flags)
