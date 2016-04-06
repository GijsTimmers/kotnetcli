#!/usr/bin/python2
# -*- coding: utf-8 -*-
##
## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck
##
## Licence:         GPLv3
##
## kotnetcli is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## kotnetcli is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with kotnetcli.  If not, see <http://www.gnu.org/licenses/>.

# HACK to include to be able to import from .. http://stackoverflow.com/a/21784070
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import rccodes
import cgi

## dummy authentication database
#TODO read in a yaml file as test database --> also write the number of IP connections...

institutions    = ['kuleuven', 'kotnetext', 'kuleuven-campusnet']
dummy_db        = { 'dummy_user' : {'pwd': 'dummy_password', 'download': 75, 'upload': 90},
                    'foo'        : {'pwd': 'bar', 'download': 20, 'upload': 60},
                    'jo'         : {'pwd': 'very_secret', 'download': 100, 'upload': 100},
                    'gijs'       : {'pwd': 'wies', 'download': 0, 'upload': 0}
                  }

## parse CGI arguments

form    = cgi.FieldStorage()
inst    = form.getfirst('inst')
lang    = form.getfirst('lang')
submit  = form.getfirst('submit')
uid     = form.getfirst('uid')
#TODO wayf2 should use a random int and write it as a uid-specific key in the yaml db file
pwd     = form.getfirst('pwd123')

## prepare HTML response (including rccode and percentages)
##TODO mimic the real HTML page returned by kotnetlogin server as closely as possible

if inst not in institutions:
    rccode = rccodes.RC_INVALID_INSTITUTION
elif uid not in dummy_db:
    rccode = rccodes.RC_LOGIN_INVALID_USERNAME
elif not (pwd == dummy_db[uid]['pwd']):
    rccode = rccodes.RC_LOGIN_INVALID_PASSWORD
else:
    rccode = rccodes.RC_LOGIN_SUCCESS

download = dummy_db[uid]['download']
upload   = dummy_db[uid]['upload']

print "Content-type: text/html"
print
print "<head>"
print "<title>Dummy server-side netlogin CGI script </title>"
print "<head/>"
print "<body>"
print "<p>Hello World!</p>"
print "<p>netlogin CGI script was requested to '{}' for user '{}' from institution '{}' with language '{}'</p>".format(submit,uid,inst,lang)
print '<p><!-- weblogin: rc={} --></p>'.format(rccode)
print '<p><!-- another comment --></p>'.format(rccode)
print '<p><!-- another comment --></p>'.format(rccode)
print '<p><!-- another comment --></p>'.format(rccode)
print '<p><!-- another comment --></p>'.format(rccode)
print '<p><!-- another comment --></p>'.format(rccode)
print '<p><!-- download percentage is {} 100 --></p>'.format(download)
print '<p><!-- upload percentage is {} 100 --></p>'.format(upload)
print "</body>"
