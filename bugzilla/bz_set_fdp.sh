#!/bin/sh

for bug in "$@"
do
	./bz_set_flags.py "$bug" fast-datapath-rhel-8 +
done
