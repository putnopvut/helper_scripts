#! /bin/sh

OLD_IFS=$IFS
IFS=$'\n'
BUGS_ARRAY=()
BUGS=$(./bz_search_bugs.py --status=NEW,ASSIGNED --component=OVN,ovn2.13,ovn2.11 --summary="RFE")
BUGS_ARRAY+=( $BUGS )

for bug in "${BUGS_ARRAY[@]}"
do
	./bz_update_keywords.py --action=add "$bug" FutureFeature
done
IFS=$OLD_IFS
