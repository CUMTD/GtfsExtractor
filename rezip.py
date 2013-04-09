#!/usr/bin/python

import os, sys
from zipfile import ZipFile

args = sys.argv[1:]

if len(args) != 2:
	print "Usage: %s gtfs-directory output-file" % sys.argv[0]
	exit(1)

with ZipFile(args[1], 'w') as zipfile:
	for root, dirs, files in os.walk(args[0]):
		for file in files:
			zipfile.write(os.path.join(root, file), file)
