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

import cgi
from random import randint

form    = cgi.FieldStorage()
inst    = form.getfirst('inst')
lang    = form.getfirst('lang')
submit  = form.getfirst('submit')

##TODO mimic the real HTML page returned by kotnetlogin server as closely as possible
## only the password field is relevant for kotnetcli
print "Content-type: text/html"
print
print "<head>"
print "<title>Dummy server-side wayf2 CGI script </title>"
print "<head/>"
print "<body>"
print "<p>Hello World!</p>"
print "<p>wayf2 CGI script was requested to '{}' for institution '{}' with language '{}'</p>".format(submit,inst,lang)
print '<p>name="pwd123"</p>'#.format(randint(0,999))
print "</body>"
