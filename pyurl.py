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
# Accept URL to be shortened
# Add data sanitizaion for MySQL; people are mean, yo
# Setup for Web
# Get someone to pay for a URL

### Import necessary modules ###
# Import random to grab random words
# Import MySQLdb to use mysql (odd right?)

import random
import MySQLdb

# URL to be shortened, supplied by users via webform
# This is a placeholder until that function is built
victim = "http://long.urls.are.bad.org/and-they-should-feel-bad?user=zoidberg&argument=why_not"
# Netid and date placeholders until those are built
netid = "phil.fry@planetexpress.com"
date = "2013-11-10 10:50:00"
# Set our hostname for the URL
host = "http://planetexpress.com/"

def pyurl():
    """
    Main function
    """

    uri = mkuri()
    url = "%s%s" % (host, uri)

    # This is what we give the user to hand out
    print url
    
    # Pass our info and verify that it's not already in use in MySQL
    verify_N_write(uri)


def mkuri():
    """
    Generate a random URI

    Capital and lowercase alphanumeric gets us a ton of potential URIs.We"ll
    remove some confusing numbers and letters, (0,O,o,1,l), leaving us 57
    potential characters to use.  Assuming a 6 character URI we get 57^6, or
    34,296,447,249 available URLs.
    """

    characters = "abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789"

    myuri = []
    while (len(myuri) < 6):
        myuri.append(random.choice(characters))

    uri = "".join(myuri)
    return uri


def verify_N_write(uri):
    """
    Check that the generated URI is not already in use, and then write it to
    the database.
    """

    # Get the global variable here
    global cursor
    global netid
    global date
    global host

    # The SQL statement - fill in the values further down
    do_sql_insert = """INSERT INTO DB.TABLE (source_uri, target_url, netid, created 
                       VALUES ('%s', '%s', '%s', '%s')"""

    # Setup the Database connection
    database = MySQLdb.connect(host="localhost",
                               user="USER",
                               passwd="PASS",
                               db="DB")
    
    # Create the database cursor
    cursor = database.cursor()

    # Keep trying until we're successful (with 39 Billion chances, we will be)
    while True:
        try:
            count = cursor.execute(do_sql_insert % (uri, victim, netid, date))
            database.commit()
            #logging.warn("%d", count)
            print "%d" % count
            #logging.info("inserted values %s, %s, %s, %s into DB.TABLE" 
            #             % (uri, victim, netid, date))
            print "Inserted values %s, %s, %s, %s into DB.TABLE" % (uri, victim, netid, date)
            # We were successful down this branch, so break out of the while loop
            break
        except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values")
                print "Failed to insert values into DB.TABLE"
    # Close the DB connection correctly so we don't have MySQL freak out
    cursor.close()


# DO IT!
pyurl()
