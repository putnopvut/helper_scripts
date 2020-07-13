#!/usr/bin/env python

from errata_tool import Erratum
import argparse
import sys
import utilities

parser = argparse.ArgumentParser()
parser.add_argument("build")
parser.add_argument("--errata_type",
                    choices=["RHSA", "RHBA", "RHEA"],
                    default="RHBA")
parser.add_argument("--owner_email",
                    default="mmichels@redhat.com")
parser.add_argument("--security_impact",
                    choices=["None",
                             "Low",
                             "Moderate",
                             "Important",
                             "Critical"],
                    default="None")
parser.add_argument("--bugs", nargs='*')
args = parser.parse_args()

package = args.build.split('-')[0]

if args.build.endswith(".el7fdp"):
    release = "Fast-Datapath-RHEL-7"
elif args.build.endswith(".el8fdp"):
    release = "Fast-Datapath-RHEL-8"
else:
    print("Invalid build specified (it must ends with .el{7,8}fdp).")
    sys.exit(1)

synopsis = package

topic = \
f"""An update for {package} is now available in Fast Datapath for Red Hat
Enterprise Linux {release[-1]}."""

description = \
"""OVN, the Open Virtual Network, is a system to support virtual network
abstraction.  OVN complements the existing capabilities of OVS to add native
support for virtual network abstractions, such as virtual L2 and L3 overlays
and security groups."""

solution = \
f"""Before applying this update, make sure all previously released errata
relevant to your system have been applied.

For details on how to apply this update, refer to:

https://access.redhat.com/articles/11258

Users of {package} are advised to upgrade to these updated packages, which fix"""

if args.errata_type == "RHEA":
    synopsis += " enhancement update"
    solution += "these bugs and add these enhancements."
elif args.errata_type == "RHBA":
    synopsis += " bug fix and enhancement update"
    solution += "these bugs."
elif args.errata_type == "RHSA":
    pass

# Ensure bugs are in proper state (MODIFIED or VERIFIED) and that they have
# the appropriate rhel-fast-datapath flag set.
s = utilities.open_session()
bz_bugs = utilities.get_bz_bugs(s, args.bugs)
for bug in bz_bugs:
    if bug['status'] != 'MODIFIED' and bug['status'] != 'VERIFIED':
        utilities.update_bz(s, bug['id'], json={'status': 'MODIFIED'})
    utilities.set_bz_flag(s, bug['id'],
                          f'fast-datapath-rhel-{release[-1]}', '+')

e = Erratum(product='Fast-Datapath',
            release=release,
            errata_type=args.errata_type,
            security_impact=args.security_impact,
            synopsis=synopsis,
            topic=topic,
            description=description,
            solution=solution,
            qe_email='ralongi@redhat.com',
            qe_group='OVS QE',
            owner_email=args.owner_email,
            manager_email='ship-list@redhat.com')

e.addBugs(args.bugs)
e.commit()
e.addBuilds([args.build], release=f"RHEL-{release[-1]}-Fast-Datapath")
print(e.url())
