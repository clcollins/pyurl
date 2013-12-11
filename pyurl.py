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

# Set our hostname for the URL
host = 'http://foo.com/'


def pyurl():
    """
    Main runner
    """

    url = []
    url.append(host)
    url.append(mkuri())

    print ''.join(url)


def mkuri():
    """
    Generate a random URI

    Capital and lowercase alphanumeric gets us a ton of potential URIs.We'll
    remove some confusing numbers and letters, (0,O,o,1,l), leaving us 57
    potential characters to use.  Assuming a 6 character URI we get 57^6, or
    34,296,447,249 available URLs.
    """

    characters = 'abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789'

    myuri = []
    while (len(myuri) < 6):
        myuri.append(random.choice(characters))
        if debug:
            print 'Pass %d: %s' % (len(myuri), myuri)

    return ''.join(myuri)


pyurl()
