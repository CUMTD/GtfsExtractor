#!/usr/bin/env python

# GTFS Extractor
#
# Given a GTFS feed and a list of routes, extracts a smaller GTFS feed that
# contains only the information needed for those routes
#
# (c) 2013, Champaign-Urbana Mass Transit District
# See the accompanying LICENSE.txt for more information

import os, sys, shutil, re
from os.path import abspath, expanduser

script_version = '0.8'


# utility functions

def normalize_path(path):
	return abspath(expanduser(path)) + '/'

def csv_field(line, field):
	return re.sub(r'[\r\n]{1,2}$', '', line.split(',')[field])

def dump_to_file(string, filename):
	with open(output_directory + filename, 'w') as out_file:
		out_file.write(string)

def debug(text):
	if verbose:
		print >> sys.stderr, text

# print help information

def version_text():
	old_out = sys.stdout
	sys.stdout = sys.stderr

	print 'GTFS Extractor %s' % script_version
	print 'https://github.com/cumtd/gtfs-extractor'
	print '(c) 2013, Champaign-Urbana Mass Transit District'
	print 'See the file LICENSE.txt for more information'

	sys.stdout = old_out

def help_text():
	version_text()

	old_out = sys.stdout
	sys.stdout = sys.stderr

	print
	print "usage: %s [--verbose] input-directory output-directory route-id [route-id ...]" % sys.argv[0]

	sys.stdout = old_out


# process command-line arguments

args = sys.argv
verbose = False

if '-v' in args or '--version' in args:
	version_text()
	exit()

if len(args) < 4 or '-h' in args or '--help' in args:
	help_text()
	exit()

if args[1] == '--verbose':
	verbose = True
	del args[1]

input_directory = normalize_path(args[1])
output_directory = normalize_path(args[2])

routes = set(args[3:])
debug('Using routes "%s"' % '", "'.join(list(routes)))

# create the output directory

if not os.path.exists(output_directory):
	debug('Creating the directory "%s"' % output_directory)
	os.mkdir(output_directory)

files_to_copy = ['agency.txt', 'fare_attributes.txt', 'fare_rules.txt', 'frequencies.txt', 'transfers.txt', 'feed_info.txt']

for f in files_to_copy:
	debug('Copying %s' % f)
	try:
		shutil.copy(input_directory + f, output_directory)
	except IOError as e:
		debug('    There is no %s in the input' % f)


# go through the files

debug('Processing routes.txt')
with open(input_directory + 'routes.txt') as routes_file:
	new_routes_file = ''

	first_line = True
	for line in routes_file:
		if first_line:
			new_routes_file += line
			first_line = False
		elif csv_field(line, 0) in routes:
			new_routes_file += line
	
	dump_to_file(new_routes_file, 'routes.txt')

services = set()
trips = set()
shapes = set()

debug('Processing trips.txt')
with open(input_directory + 'trips.txt') as trips_file:
	new_trips_file = ''

	first_line = True
	for line in trips_file:
		if first_line:
			new_trips_file += line
			first_line = False
		elif csv_field(line, 0) in routes:
			new_trips_file += line
			services.add(csv_field(line, 1))
			trips.add(csv_field(line, 2))
			shapes.add(csv_field(line, 6))
	
	dump_to_file(new_trips_file, 'trips.txt')

debug('Processing calendar.txt')
with open(input_directory + 'calendar.txt') as calendar_file:
	new_calendar_file = ''

	first_line = True
	for line in calendar_file:
		if first_line:
			new_calendar_file += line
			first_line = False
		elif csv_field(line, 0) in services:
			new_calendar_file += line

	dump_to_file(new_calendar_file, 'calendar.txt')

debug('Processing calendar_dates.txt')
with open(input_directory + 'calendar_dates.txt') as calendar_dates_file:
	new_calendar_dates_file = ''

	first_line = True
	for line in calendar_dates_file:
		if first_line:
			new_calendar_dates_file += line
			first_line = False
		elif csv_field(line, 0) in services:
			new_calendar_dates_file += line

	dump_to_file(new_calendar_dates_file, 'calendar_dates.txt')

debug('Processing shapes.txt')
with open(input_directory + 'shapes.txt') as shapes_file:
	new_shapes_file = ''

	first_line = True
	for line in shapes_file:
		if first_line:
			new_shapes_file += line
			first_line = False
		elif csv_field(line, 0) in shapes:
			new_shapes_file += line

	dump_to_file(new_shapes_file, 'shapes.txt')

stops = set()

debug('Processing stop_times.txt')
with open(input_directory + 'stop_times.txt') as stop_times_file:
	new_stop_times_file = ''

	first_line = True
	for line in stop_times_file:
		if first_line:
			new_stop_times_file += line
			first_line = False
		elif csv_field(line, 0) in trips:
			new_stop_times_file += line
			stops.add(csv_field(line, 3))

	dump_to_file(new_stop_times_file, 'stop_times.txt')

parent_stops = {re.sub(r':[0-9]+', '', stop) for stop in stops}

debug('Processing stops.txt')
with open(input_directory + 'stops.txt') as stops_file:
	new_stops_file = ''

	first_line = True
	for line in stops_file:
		if first_line:
			new_stops_file += line
			first_line = False
		elif csv_field(line, 0) in stops or csv_field(line, 0) in parent_stops:
			new_stops_file += line

	dump_to_file(new_stops_file, 'stops.txt')


# vim: ts=4
