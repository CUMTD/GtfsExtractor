# GtfsExtractor

Given a [GTFS feed](https://developers.google.com/transit/gtfs/reference) and a list of routes, this script generates a (presumably smaller) GTFS feed that contains the data only for those routes. (For example, the generated `stops.txt` will contain only the stops for the routes you’ve specified.)

## Why is this useful?

The GTFS feed for even a smaller transit agency can consist of hundreds of thousands of lines of text. Testing the GTFS-related parts of a transit workflow doesn't generally require you to use a *full* data set, just a *coherent* data set--one in which, for example, all of the stops mentioned in the `stop_times` file are properly defined in the `stops` file. This script takes a list of routes as input and pulls out just those parts of your GTFS feed that are actually referred to by those routes. This can result in a significant space savings:

<table>
	<thead>	
		<tr>
			<td rowspan="2">File</td>
			<td colspan="2">Full feed</td>
			<td colspan="2">Just two routes</td>
		</tr>
		<tr>
			<td>Lines</td>
			<td>Size</td>
			<td>Lines</td>
			<td>Size</td>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>calendar_dates.txt</td>
			<td>11,515</td>
			<td>214 KiB</td>
			<td>669</td>
			<td>11 KiB</td>
		</tr>
		<tr>
			<td>calendar.txt</td>
			<td>289</td>
			<td>12 KiB</td>
			<td>11</td>
			<td>465 B</td>
		</tr>
		<tr>
			<td>routes.txt</td>
			<td>68</td>
			<td>3.7 KiB</td>
			<td>3</td>
			<td>199 B</td>
		</tr>
		<tr>
			<td>shapes.txt</td>
			<td>1,151,937</td>
			<td>67 MiB</td>
			<td>48,022</td>
			<td>2.7 MiB</td>
		</tr>
		<tr>
			<td>stops.txt</td>
			<td>3,951</td>
			<td>531 KiB</td>
			<td>325</td>
			<td>43 KiB</td>
		</tr>
		<tr>
			<td>stop_times.txt</td>
			<td>252,460</td>
			<td>19 MiB</td>
			<td>5,768</td>
			<td>447 KiB</td>
		</tr>
		<tr>
			<td>trips.txt</td>
			<td>5,736</td>
			<td>586 KiB</td>
			<td>125</td>
			<td>12 KiB</td>
		</tr>
	</tbody>
</table>

Of course, your results will vary.

## Usage

`extractor.py [-z] input_path output_path route_id [route_id ...]`

The `input_path` and `output_path` specify where the GTFS files will be read from and written to. For convenience, the script can operate either on directories full of files (the default) or the zipped versions of these directories. For the latter behavior, pass the `-z` flag; then the script will expect `input_path` to be a ZIP file and it will emit a ZIP file to `output_path`.

The `route_id` argument(s) correspond to the route IDs given in `routes.txt`. These are the IDs of the routes for which information will be kept. As a special case, if you pass the word `all` instead of route IDs, information for all of the routes listed in `routes.txt` will be kept. (This is useful to make sure that there are no extraneous stops, trips, etc. in your data.)

The script has only been tested with Python 2.7, but is probably compatible with other versions of Python. For known issues, see the “Issues” tab on [the GitHub project page](https://github.com/CUMTD/GtfsExtractor).

## License

Copyright (c) 2013, Champaign–Urbana Mass Transit District. All rights reserved.

Developed by: Benjamin Esham, [Champaign–Urbana Mass Transit District](http://www.cumtd.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal with the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimers.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
* Neither the name of the Champaign-Urbana Mass Transit District nor the names of its contributors may be used to endorse or promote products derived from this Software without specific prior written permission.

**The software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the contributors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings with the software.**
