#!/usr/bin/env python
# Copyright (C) 2013 Chris Collins
#
# This file is part of Pyurl.
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

#################################
### ENVIRONMENT SPECIFIC INFO ###
#################################

# Fill these out to match your
# local environment's setup
CONFFILE='/etc/httpd/conf.d/pyurl-rewrites'
HOST = "localhost"
USER = ""
PASS = ""
DB = ""
TABLE = ""

##################################
### That's it, no more editing ###
##################################

### Import necessary modules ###
# Import MySQLDB to interact with the database
# Import urllib for unquote_plus, to write webserver-acceptable URLs to the DB

import MySQLdb
import urllib

db = MySQLdb.connect(host = HOST,
                     user = USER,
                     passwd = PASS,
                     db = DB)

cursor = db.cursor()

cursor.execute("SELECT CONCAT('RewriteRule ^/', source_uri, '$ ', target_url, ' [R=301,L]') FROM %s.%s;" % (DB, TABLE))

target = open(CONFFILE, "w")
target.write("# File created by pyurl-cron.py \n")
for row in cursor.fetchall():
    target.write(urllib.unquote_plus(row[0]) + "\n")

target.close()

