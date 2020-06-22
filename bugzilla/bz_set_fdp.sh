#!/bin/sh

for bug in "$@"
do
	./bz_set_flags.py "$bug" fast-datapath-rhel-7 +
done
