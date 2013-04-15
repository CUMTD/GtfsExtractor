# GtfsExtractor

Given a GTFS feed and a list of route IDs, this script generates a (presumably smaller) GTFS feed that contains the data only for those routes. (For example, the generated `stops.txt` will contain only the stops for the routes you've specified.)

## Usage

`extractor.py input_directory output_directory route_id [route_id ...]`

where

* `input_directory` is a directory containing your GTFS files.
* `output_directory` is where the new files will be written. This directory will be created if it doesn't exist.
* the `route_id` arguments correspond to the `route_id` keys from the `routes.txt` file for which information should be kept.

The script has only been tested with Python 2.7, but is probably compatible with other versions of Python. For known issues, see the "Issues" tab on the GitHub project page.

## License

Copyright (c) 2013, Champaign-Urbana Mass Transit District. All rights reserved.

Developed by: Benjamin Esham, [Champaign-Urbana Mass Transit District](http://www.cumtd.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal with
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimers.  Redistributions in binary
form must reproduce the above copyright notice, this list of conditions and the
following disclaimers in the documentation and/or other materials provided with
the distribution.  Neither the name of the Champaign-Urbana Mass Transit
District nor the names of its contributors may be used to endorse or promote
products derived from this Software without specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.
