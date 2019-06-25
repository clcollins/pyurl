#!/usr/bin/python
#
# pyurl
# =====
# Python-based URL shortener
#
# Chris Collins, <collins.christopher@gmail.com>
#
# v 1.0 - 2013-12-13
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
# Try to clean up error handling
# - shouldn't have to re-build the page for each error
# - maybe just a definition to call

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
DB = os.getenv("PYURL_DATABASE_NAME")
USER = os.getenv("PYURL_DATABASE_USERNAME")
PASS = os.getenv("PYURL_DATABASE_PASSWORD")

# Generic name for your usernames, eg - "login", "username"
# Could be rewritten.  This was a poor attempt at customization
SN_SLUG = os.getenv("PYURL_SN_SLUG", default="netid")

# The path to your pyurl folder
# This could be written better probably, to remove the need for this variable
LOCAL_PATH = os.getenv("PYURL_LOCAL_PATH", default="/srv/web/pyurl"

##################################
### That's it, no more editing ###
##################################

# Pyurl variables
TABLE = "shorts"  # The table to use
LOGTABLE = "access_log"


def 

## Web.py basics
# Tell web.py where the templates are

# Define URL handling
urls = (
    "/", "index",
    "/(.{6})", "redirect",
    "/shorten", "shorten",
    "/login", "login",
    "/metrics", "metrics",
)

## Database Connection Info
db = web.database(dbn="mysql",
                  user=USER,
                  pw=PASS,
                  db=DB)

# Err var to override
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
        ## Get the servername from the HTTP_HOST var
        server_name = web.ctx.env.get("HTTP_HOST")
            
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

        # Sanitize the input for the DB
	clean_target_url = urllib.quote_plus(target_url)

        # Check to see if there are more than 8160 characters in the request:
        # Apache LimitRequestLine Directive 
        if not len(target_url) < 4096:
            err = "\""+ target_url + "\" does not appear to be a valid URL.  Is it too long?"
            table = db.select(TABLE,
                              where="%s='%s'" % (SN_SLUG, remote_user),
                              order="created DESC")
            return render.index(table, server_name, remote_user, SN_SLUG, err)

        # Regex to check against to see if the URL is valid
        valid = re.compile(r"^(?:http|ftp)s?://"  # http:// or https://
                           r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
                           r"localhost|"  # localhost...
                           r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
                           r"(?::\d+)?"  # optional port
                           r"(?:/?|[/?]\S+)$", re.I)

        # Check to see if the unencoded URL is valid or not
        if not re.match(valid, target_url):
            err = "\"" + target_url + "\" does not appear to be a valid URL."
            table = db.select(TABLE,
                              where="%s='%s'" % (SN_SLUG, remote_user),
                              order="created DESC")
            return render.index(table, server_name, remote_user, SN_SLUG, err)

        # Otherwise, go ahead and insert it into the database
        try:
            db.insert(TABLE,
                      source_uri=mkuri(),
                      target_url=clean_target_url,
                      netid=remote_user)
        except:
            error("Failed to insert values into the database.")

        # Return to / if successful
        raise web.seeother("/")


# POST data is dropped by shibboleth if user doesn't have a session
# This class just forces a login (via Apache shib rule) and redirects
# back to the main page.
class login:
    def GET(self):
        raise web.seeother("/")


class metrics:
    def GET(self):
        """
        Some basic metrics for folks limited folks to use to get metrics about their Redirects 
        """

        ## Get the servername from the HTTP_HOST var
        server_name = web.ctx.env.get("HTTP_HOST")
        # Set to REMOTE_USER var from HTTP headers
        # or a default, if it's not there
        remote_user = web.ctx.env.get("REMOTE_USER",
                                      "")
        # render index with info from TABLE and server_name
        uris = db.query("SELECT source_uri, target_url from `%s` WHERE %s = '%s';" % (TABLE, SN_SLUG, remote_user))
        return render.metrics(uris, remote_user, server_name, SN_SLUG)


def mkuri():
    """
    Generate a random 
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


def getlogs(uri):
    """
    Pass on the uri and get the logs for it
    """

    logs = db.query("SELECT referer, agent, request_time, time_stamp from `%s` WHERE request_uri = CONCAT('/', '%s') ORDER BY time_stamp DESC;" % (LOGTABLE, uri))

    return logs


app = web.application(urls, globals())
render = web.template.render(LOCAL_PATH + "/templates/", globals={"uncode": uncode,"getlogs": getlogs})

curdir = os.path.dirname(__file__)
session = web.session.Session(
    app, web.session.DiskStore(
        os.path.join(curdir, "%s/sessions" % LOCAL_PATH)),)

application = app.wsgifunc()
