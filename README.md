# GtfsExtractor

Given a [GTFS feed](https://developers.google.com/transit/gtfs/reference) and a list of routes, this script generates a (presumably smaller) GTFS feed that contains the data only for those routes. (For example, the generated `stops.txt` will contain only the stops for the routes you’ve specified.)

## Usage

`extractor.py input_directory output_directory route_id [route_id ...]`

where

* `input_directory` is a directory containing your GTFS files.
* `output_directory` is where the new files will be written. This directory will be created if it doesn’t exist.
* the `route_id` arguments correspond to the `route_id` keys from the `routes.txt` file for which information should be kept.

The script has only been tested with Python 2.7, but is probably compatible with other versions of Python. For known issues, see the “Issues” tab on [the GitHub project page](https://github.com/CUMTD/GtfsExtractor).

## License

Copyright (c) 2013, Champaign–Urbana Mass Transit District. All rights reserved.

Developed by: Benjamin Esham, [Champaign–Urbana Mass Transit District](http://www.cumtd.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal with the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimers.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
* Neither the name of the Champaign-Urbana Mass Transit District nor the names of its contributors may be used to endorse or promote products derived from this Software without specific prior written permission.

**The software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the contributors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings with the software.**
