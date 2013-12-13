#!/usr/bin/python
#
# pyurl
# =====
# Python-based URL shortener
#
# Chris Collins, <christopher.collins@duke.edu>
#
# v0.2 - 2013-12-13
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

### TODO ###
# Display Short URL and Target URL to user on POST
# Display All User's past target and short urls
# Figure out how to preserve POST data through session initiation
# Figure out error handling for MySQL
# Add data sanitizaion for MySQL; people are mean, yo
# Get someone to pay for a URL

### Import necessary modules ###
# Import random to grab random words
# Import web for web.py wsgi support
# Import os for current dir sessions support

import random
import web
import os

#################################
### ENVIRONMENT SPECIFIC INFO ###
#################################

# Fill these out to match your
# local environment's setup

# The database name
DB = ''
# The table to use
TABLE = ''
# The database user
USER = ''
# The database user's password
PASS = ''
# The path to your pyurl folder
LOCAL_PATH = ''
# Generic name for your usernames
# eg - "login", "username", "user_id"
SN_SLUG = ""

##################################
### That's it, no more editing ###
##################################

### Define some global variables ###
debug = True

## Web.py basics
# Tell web.py where the templates are
render = web.template.render('%s/templates/' % LOCAL_PATH)

# Define URL handling
urls = (
    '/', 'index',
    '/shorten', 'shorten',
    '/login', 'login'
)

## Database Connection Info
db = web.database(dbn='mysql',
                  user=USER,
                  pw=PASS,
                  db=DB)


### Classes and Functions ###
# Base class; renders index page
class index:
    def GET(self):
        ## Get the servername from the HTTP_HOST var
        server_name = web.ctx.env.get('HTTP_HOST')
        # Set to REMOTE_USER var from HTTP headers
        # so we can force users to login first
        remote_user = web.ctx.env.get('REMOTE_USER',
                                      '')

        # Get info from the TABLE
        table = db.select(TABLE)
        # render index with info from TABLE and server_name
        return render.index(table, server_name, remote_user, SN_SLUG, debug)


# Class to handle POST
class shorten:
    def POST(self):
        # Set to REMOTE_USER var from HTTP headers
        # or a default, if it's not there
        remote_user = web.ctx.env.get('REMOTE_USER',
                                      '')

        # Get the input from the web form
        i = web.input()

        # Update the database
        # Call mkuri() to generate the URI on POST
        # Gather the long URL from the user
        # remote_user set above
        try:
            n = db.insert(TABLE,
                          source_uri=mkuri(),
                          target_url=i.target_url,
                          netid=remote_user)
        # TODO: This doesn't actually work.
        # No IntregityError in the web.py
        except db.IntegrityError:
            return "Failed to insert values into", DB.TABLE

        # Return to /
        raise web.seeother('/')


# POST data is dropped by shibboleth if user doesn't have a session
# This class just forces a login (via Apache shib rule) and redirects
# back to the main page.
class login:
    def GET(self):
        raise web.seeother('/')


# Function to generate 6 character URIs
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


app = web.application(urls, globals())

curdir = os.path.dirname(__file__)
session = web.session.Session(
    app, web.session.DiskStore(
        os.path.join(curdir, '%s/sessions' % LOCAL_PATH)),)

application = app.wsgifunc()
