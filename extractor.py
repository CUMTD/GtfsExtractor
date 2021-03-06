#!/usr/bin/env python

# GTFS Extractor
#
# Given a GTFS feed and a list of routes, extracts a smaller GTFS feed that
# contains only the information needed for those routes
#
# (c) 2013, Champaign-Urbana Mass Transit District
# See the "License" section in the accompanying README.md for more information.
#
# https://github.com/CUMTD/GtfsExtractor

import os, sys, shutil, re, argparse
from os.path import abspath, expanduser
from tempfile import mkdtemp
from zipfile import ZipFile, ZIP_DEFLATED

script_version = '0.8'
verbose = False


# utility functions

def normalize_path(path):
	return abspath(expanduser(path))

def fields_dict(line):
	fields = line.split(',')
	return {fields[i].rstrip(): i for i in range(len(fields))}

def csv_field(line, field):
	return line.split(',')[field].rstrip()

def dump_to_file(string, filename):
	with open(output_directory + filename, 'w') as out_file:
		out_file.write(string)

def debug(text):
	if verbose:
		print >> sys.stderr, text


# process command-line arguments

parser = argparse.ArgumentParser(description = 'Extract a GTFS feed that contains only some routes',
	epilog = 'https://github.com/CUMTD/GtfsExtractor')
parser.add_argument('-v', '--verbose', action = 'store_true',
	help = 'narrate what\'s going on')
parser.add_argument('-z', '--zip', action = 'store_true',
	help = 'read from and write to ZIP files rather than directories')
parser.add_argument('--version', action = 'version',
	version = 'GTFS Extractor %s' % script_version,
	help = 'show version information and exit')
parser.add_argument('input_path', type = str,
	help = 'directory or zip file containing input files')
parser.add_argument('output_path', type = str,
	help = 'directory or zip file where output will be written')
parser.add_argument('route_id', type = str, nargs = '+',
	help = 'route(s) whose data should be included, or the keyword "all" to include all routes')

args = parser.parse_args()

verbose = args.verbose

routes = set(args.route_id)
all_routes = routes == {'all'}
if all_routes:
	debug('Using all routes')
else:
	debug('Using routes "%s"' % '", "'.join(list(routes)))

# if the input is a zip file, "convert" it to a directory first

input_path = normalize_path(args.input_path)
output_path = normalize_path(args.output_path)

if args.zip:
	input_directory = mkdtemp() + '/'
	debug('Extracting %s to %s' % (input_path, input_directory))
	with ZipFile(input_path, 'r') as z:
		z.extractall(input_directory)
	
	output_directory = mkdtemp() + '/'
else:
	input_directory = input_path + '/'
	output_directory = output_path + '/'

# create the output directory

if not os.path.exists(output_directory):
	debug('Creating the directory "%s"' % output_directory)
	os.mkdir(output_directory)

files_to_copy = ['agency.txt', 'feed_info.txt']

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
			fields = fields_dict(line)
			new_routes_file += line
			first_line = False
		elif line.rstrip() == '':
			next
		else:
			if all_routes:
				routes.add(csv_field(line, fields['route_id']))
				new_routes_file += line
			elif csv_field(line, fields['route_id']) in routes:
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
			fields = fields_dict(line)
			new_trips_file += line
			first_line = False
		elif line.rstrip() == '':
			next
		elif csv_field(line, fields['route_id']) in routes:
			new_trips_file += line
			services.add(csv_field(line, fields['service_id']))
			trips.add(csv_field(line, fields['trip_id']))
			shapes.add(csv_field(line, fields['shape_id']))
	
	dump_to_file(new_trips_file, 'trips.txt')

debug('Processing calendar.txt')
with open(input_directory + 'calendar.txt') as calendar_file:
	new_calendar_file = ''

	first_line = True
	for line in calendar_file:
		if first_line:
			fields = fields_dict(line)
			new_calendar_file += line
			first_line = False
		elif line.rstrip() == '':
			next
		elif csv_field(line, fields['service_id']) in services:
			new_calendar_file += line

	dump_to_file(new_calendar_file, 'calendar.txt')

debug('Processing calendar_dates.txt')
try:
	with open(input_directory + 'calendar_dates.txt') as calendar_dates_file:
		new_calendar_dates_file = ''

		first_line = True
		for line in calendar_dates_file:
			if first_line:
				fields = fields_dict(line)
				new_calendar_dates_file += line
				first_line = False
			elif line.rstrip() == '':
				next
			elif csv_field(line, fields['service_id']) in services:
				new_calendar_dates_file += line

		dump_to_file(new_calendar_dates_file, 'calendar_dates.txt')
except IOError as e:
	debug('    There is no calendar_dates.txt in the input')

debug('Processing frequencies.txt')
try:
	with open(input_directory + 'frequencies.txt') as frequencies_file:
		new_frequencies_file = ''

		first_line = True
		for line in frequencies_file:
			if first_line:
				fields = fields_dict(line)
				new_frequencies_file += line
				first_line = False
			elif line.rstrip() == '':
				next
			elif csv_field(line, fields['trip_id']) in services:
				new_frequencies_file += line

		dump_to_file(new_frequencies_file, 'frequencies.txt')
except IOError as e:
	debug('    There is no frequencies.txt in the input')

debug('Processing shapes.txt')
try:
	with open(input_directory + 'shapes.txt') as shapes_file:
		new_shapes_file = ''

		first_line = True
		for line in shapes_file:
			if first_line:
				fields = fields_dict(line)
				new_shapes_file += line
				first_line = False
			elif line.rstrip() == '':
				next
			elif csv_field(line, fields['shape_id']) in shapes:
				new_shapes_file += line

		dump_to_file(new_shapes_file, 'shapes.txt')
except IOError as e:
	debug('    There is no shapes.txt in the input')

stops = set()

debug('Processing stop_times.txt')
with open(input_directory + 'stop_times.txt') as stop_times_file:
	new_stop_times_file = ''

	first_line = True
	for line in stop_times_file:
		if first_line:
			fields = fields_dict(line)
			new_stop_times_file += line
			first_line = False
		elif line.rstrip() == '':
			next
		elif csv_field(line, fields['trip_id']) in trips:
			new_stop_times_file += line
			stops.add(csv_field(line, fields['stop_id']))

	dump_to_file(new_stop_times_file, 'stop_times.txt')

parent_stops = {re.sub(r':[0-9]+', '', stop) for stop in stops}
all_stops = stops.union(parent_stops)
zone_ids = set()

debug('Processing stops.txt')
with open(input_directory + 'stops.txt') as stops_file:
	new_stops_file = ''
	parent_stations = set()

	first_line = True
	for line in stops_file:
		if first_line:
			fields = fields_dict(line)
			new_stops_file += line
			first_line = False
		elif line.rstrip() == '':
			next
		elif csv_field(line, fields['stop_id']) in all_stops:
			new_stops_file += line
			zone_ids.add(csv_field(line, fields['zone_id']))
			if 'parent_station' in fields and csv_field(line, fields['parent_station']) != '':
				parent_stations.add(csv_field(line, fields['parent_station']))
	
	stops_file.seek(0)
	for line in stops_file:
		if csv_field(line, fields['stop_id']) in parent_stations:
			new_stops_file += line

	dump_to_file(new_stops_file, 'stops.txt')

fare_ids = set()

debug('Processing fare_rules.txt')
try:
	with open(input_directory + 'fare_rules.txt') as fare_rules_file:
		new_fare_rules_file = ''

		first_line = True
		for line in fare_rules_file:
			if first_line:
				fields = fields_dict(line)
				new_fare_rules_file += line
				first_line = False
			elif line.rstrip() == '':
				next
			elif (csv_field(line, fields['route_id']) != '' and csv_field(line, fields['route_id']) in routes) or (csv_field(line, fields['route_id']) == '' and (csv_field(line, fields['origin_id']) in zone_ids or csv_field(line, fields['destination_id']) in zone_ids or csv_field(line, fields['contains_id']) in zone_ids)):
				new_fare_rules_file += line
				fare_ids.add(csv_field(line, fields['fare_id']))

		dump_to_file(new_fare_rules_file, 'fare_rules.txt')
except IOError as e:
	debug('    There is no fare_rules.txt in the input')

debug('Processing fare_attributes.txt')
try:
	with open(input_directory + 'fare_attributes.txt') as fare_attributes_file:
		new_fare_attributes_file = ''

		first_line = True
		for line in fare_attributes_file:
			if first_line:
				fields = fields_dict(line)
				new_fare_attributes_file += line
				first_line = False
			elif line.rstrip() == '':
				next
			elif csv_field(line, fields['fare_id']) in fare_ids:
				new_fare_attributes_file += line
		
		dump_to_file(new_fare_attributes_file, 'fare_attributes.txt')
except IOError as e:
	debug('    There is no fare_attributes.txt in the input')

debug('Processing transfers.txt')
try:
	with open(input_directory + 'transfers.txt') as transfers_file:
		new_transfers_file = ''

		first_line = True
		for line in transfers_file:
			if first_line:
				fields = fields_dict(line)
				new_transfers_file += line
				first_line = False
			elif line.rstrip() == '':
				next
			elif csv_field(line, fields['from_stop_id']) in all_stops and csv_field(line, fields['to_stop_id']):
				new_transfers_file += line
		
		dump_to_file(new_transfers_file, 'transfers.txt')
except IOError as e:
	debug('    There is no transfers.txt in the input')
		

# write the output into a zip file if necessary

if args.zip:
	debug('Compressing %s to %s' % (output_directory, output_path))
	with ZipFile(args.output_path, 'w', ZIP_DEFLATED) as z:
		for root, dirs, files in os.walk(output_directory):
			for file in files:
				z.write(os.path.join(root, file), file)
	
	debug('Unlinking temporary directories')
	shutil.rmtree(input_directory)
	shutil.rmtree(output_directory)


# vim: ts=4
