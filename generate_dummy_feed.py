#!/usr/bin/env python

import os, shutil, re


def csv_field(line, field):
	return re.sub(r'[\r\n]{1,2}$', '', line.split(',')[field])

def dump_to_file(string, filename):
	with open(filename, 'w') as out_file:
		out_file.write(string)


# options

routes = {'AIR BUS WEEKEND'}
new_directory = 'gtfs-modified'


# create the output directory

if not os.path.exists(new_directory):
		os.mkdir(new_directory)

shutil.copy('gtfs/agency.txt', new_directory)


# go through the files

with open('gtfs/routes.txt') as routes_file:
	new_routes_file = ''

	first_line = True
	for line in routes_file:
		if first_line:
			new_routes_file += line
			first_line = False
		elif csv_field(line, 0) in routes:
			new_routes_file += line
	
	dump_to_file(new_routes_file, new_directory + '/routes.txt')

services = set()

with open('gtfs/trips.txt') as trips_file:
	new_trips_file = ''

	first_line = True
	for line in trips_file:
		if first_line:
			new_trips_file += line
			first_line = False
		elif csv_field(line, 0) in routes:
			new_trips_file += line
			services.add(csv_field(line, 1))
	
	dump_to_file(new_trips_file, new_directory + '/trips.txt')

with open('gtfs/calendar.txt') as calendar_file:
	new_calendar_file = ''

	first_line = True
	for line in calendar_file:
		if first_line:
			new_calendar_file += line
			first_line = False
		elif csv_field(line, 0) in services:
			new_calendar_file += line

	dump_to_file(new_calendar_file, new_directory + '/calendar.txt')

with open('gtfs/calendar_dates.txt') as calendar_dates_file:
	new_calendar_dates_file = ''

	first_line = True
	for line in calendar_dates_file:
		if first_line:
			new_calendar_dates_file += line
			first_line = False
		elif csv_field(line, 0) in services:
			new_calendar_dates_file += line

	dump_to_file(new_calendar_dates_file, new_directory + '/calendar_dates.txt')

trips = set()
shapes = set()

with open('gtfs/trips.txt') as trips_file:
	new_trips_file = ''

	first_line = True
	for line in trips_file:
		if first_line:
			new_trips_file += line
			first_line = False
		elif csv_field(line, 0) in routes:
			new_trips_file += line
			trips.add(csv_field(line, 2))
			shapes.add(csv_field(line, 6))

	dump_to_file(new_trips_file, new_directory + '/trips.txt')

with open('gtfs/shapes.txt') as shapes_file:
	new_shapes_file = ''

	first_line = True
	for line in shapes_file:
		if first_line:
			new_shapes_file += line
			first_line = False
		elif csv_field(line, 0) in shapes:
			new_shapes_file += line

	dump_to_file(new_shapes_file, new_directory + '/shapes.txt')

stops = set()

with open('gtfs/stop_times.txt') as stop_times_file:
	new_stop_times_file = ''

	first_line = True
	for line in stop_times_file:
		if first_line:
			new_stop_times_file += line
			first_line = False
		elif csv_field(line, 0) in trips:
			new_stop_times_file += line
			stops.add(csv_field(line, 3))

	dump_to_file(new_stop_times_file, new_directory + '/stop_times.txt')

parent_stops = {re.sub(r':[0-9]+', '', stop) for stop in stops}

with open('gtfs/stops.txt') as stops_file:
	new_stops_file = ''

	first_line = True
	for line in stops_file:
		if first_line:
			new_stops_file += line
			first_line = False
		elif csv_field(line, 0) in stops or csv_field(line, 0) in parent_stops:
			new_stops_file += line

	dump_to_file(new_stops_file, new_directory + '/stops.txt')


# vim: ts=4
