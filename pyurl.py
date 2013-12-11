#!/usr/bin/python
#
# pyurl
# =====
# Python-based URL shortener
#
# Chris Collins, <christopher.collins@duke.edu>
#
# v.01 - 2013-12-11
#
# Copyright 2013 Chris Collins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

debug = True

### TODO ###
# Write random generator
# Connect to MySQL
# Accept URL
# Setup for Web
# Get someone to pay for a URL

### Import necessary modules ###
# Import random to grab random words

import random

def pyurl():
    """
    Main runner
    """

    if debug:
        url = '/abc123'

    print url


pyurl()
