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
# Copyright (C) 2013 Chris Collins
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
# Figure out error handling for MySQL
# Add data sanitizaion for MySQL; people are mean, yo
# Get someone to pay for a URL

### Import necessary modules ###
# Import random to grab random words
# Import web for web.py wsgi support
# Import os for current dir sessions support
# Import re for regex to validate urls
# Import urllib for url validation as well

import random
import web
import os
import re
import urllib

#################################
### ENVIRONMENT SPECIFIC INFO ###
#################################

# Fill these out to match your
# local environment's setup
DB = ""  # The database name
TABLE = ""  # The table to use
USER = ""  # The database user
PASS = ""  # The database user's password
LOCAL_PATH = ""  # The path to your pyurl folder
SN_SLUG = ""  # Generic name for your usernames, eg - "login", "username"


##################################
### That's it, no more editing ###
##################################

## Web.py basics
# Tell web.py where the templates are

# Define URL handling
urls = (
    "/", "index",
    "/(.{6})", "redirect",
    "/shorten", "shorten",
    "/login", "login"
)

## Database Connection Info
db = web.database(dbn="mysql",
                  user=USER,
                  pw=PASS,
                  db=DB)


err = None
### Classes and Functions ###
# Base class; renders index page


class index:
    def GET(self):
        ## Get the servername from the HTTP_HOST var
        server_name = web.ctx.env.get("HTTP_HOST")
        # Set to REMOTE_USER var from HTTP headers
        # so we can force users to login first
        remote_user = web.ctx.env.get("REMOTE_USER",
                                      "")
        table = db.select(TABLE,
                          where="%s='%s'" % (SN_SLUG, remote_user),
                          order="created DESC")
        # render index with info from TABLE and server_name
        return render.index(table, server_name, remote_user, SN_SLUG, err)


# Class to redirect source URIs to target URLs
class redirect:
    def GET(self, name):
        vars = dict(the_uri=name)
        target = db.select(TABLE,
                           vars,
                           what="target_url",
                           where="source_uri=$the_uri")
        for data in target:
            the_url = urllib.unquote_plus(data.target_url)
            raise web.seeother(the_url)


# Class to handle POST
class shorten:
    def POST(self):
        # Set to REMOTE_USER var from HTTP headers
        # or a default, if it's not there
        remote_user = web.ctx.env.get("REMOTE_USER",
                                      "")

        # Get the input from the web form
        i = web.input()
        target_url = i.target_url

        # Check for protocol, and add http if there's not one
        protocol = re.compile(r"^(?:http|ftp)s?://", re.I)
        if not re.match(protocol, target_url):
            target_url = "http://" + target_url

        # Regex to check against to see if the URL is valid
        valid = re.compile(r"^(?:http|ftp)s?://"  # http:// or https://
                           r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
                           r"localhost|"  # localhost...
                           r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
                           r"(?::\d+)?"  # optional port
                           r"(?:/?|[/?]\S+)$", re.I)

        # Sanitize the input for the DB
        clean_target_url = urllib.quote_plus(target_url)

        # Check to see if the unencoded URL is valid or not
        if not re.match(valid, target_url):
            # If it's not valid, use the clean_target_url just to be safe
            err = clean_target_url + " does not appear to be a valid URL."

            ## Get the servername from the HTTP_HOST var
            server_name = web.ctx.env.get("HTTP_HOST")

            # Set to REMOTE_USER var from HTTP headers
            # so we can force users to login first
            remote_user = web.ctx.env.get("REMOTE_USER",
                                          "")
            table = db.select(TABLE,
                              where="%s='%s'" % (SN_SLUG, remote_user),
                              order="created DESC")
            # render index with info from TABLE and server_name
            return render.index(table, server_name, remote_user, SN_SLUG, err)

        try:
            db.insert(TABLE,
                      source_uri=mkuri(),
                      target_url=clean_target_url,
                      netid=remote_user)
        except:
            return ("Failed to insert values into the database.")
        # Return to /
        raise web.seeother("/")


# POST data is dropped by shibboleth if user doesn't have a session
# This class just forces a login (via Apache shib rule) and redirects
# back to the main page.
class login:
    def GET(self):
        raise web.seeother("/")


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


def uncode(url):
    """
    Unencodes the target_url for display on the web, nicely
    """
    return urllib.unquote_plus(url)


app = web.application(urls, globals())
render = web.template.render(LOCAL_PATH + "/templates/", globals={"uncode": uncode})

curdir = os.path.dirname(__file__)
session = web.session.Session(
    app, web.session.DiskStore(
        os.path.join(curdir, "%s/sessions" % LOCAL_PATH)),)

application = app.wsgifunc()
