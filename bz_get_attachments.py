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

import bugzilla
import os
import sys
from pathlib import Path

URL = "bugzilla.redhat.com"
bzapi = bugzilla.Bugzilla(URL)

if len(sys.argv) < 2:
    print("Please include a BZ bug number")
    sys.exit(1)

bugno = sys.argv[1]

if not bzapi.logged_in:
    bzapi.interactive_login()

print(f"Retrieving bug {bugno}")
try:
    bug = bzapi.getbug(bugno)
except Exception:
    print(f"Failed to retrieve bug {bugno}. Exiting.")
    sys.exit(1)

path = Path(Path.home(), Path('bugzilla'), Path(bugno))

print(f"Creating directory {path} if it does not already exist")
os.makedirs(path, exist_ok=True)

print("Retrieving attachments")
atts = bug.get_attachments()
for att in atts:
    data = att['data']
    if hasattr(data, "data"):
        content = data.data
    else:
        import base64
        content = base64.decode(data)

    write_path = Path(path, Path(att['file_name']))
    with open(write_path, 'wb') as fi:
        print(f'Writing {fi.name}')
        fi.write(content)
