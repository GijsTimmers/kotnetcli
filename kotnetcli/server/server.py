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

import time
import BaseHTTPServer
import CGIHTTPServer
import ssl

import os
from ..__init__ import resolve_path

HOST_NAME   = 'localhost'
PORT_NUMBER = 8888
SRV_DIR     = resolve_path("server")

def main():
    ## Set up a simple HTTP server that listens for incoming GET/POST requests
    ## and passes them to the relevant CGI scripts to prepare the HTML response.
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), handler)

    ## The development test server is intended to run on localhost, so we can
    ## simply use a plain unencrypted HTTP connection. The following lines
    ## enables SSL, should we ever want a remote test server.
    #httpd.socket = ssl.wrap_socket (httpd.socket, certfile=CERT_FILE,
    #                                server_side=True)
    #
    ## Force the use of a subprocess for CGI scripts to ensure they have acccess
    ## to the SSL wrapped socket (see also http://stackoverflow.com/a/27303995)
    #CGIHTTPServer.CGIHTTPRequestHandler.have_fork=False

    ## Ensure the cgi-bin directory is found.
    print "cd to server directory at '{0}'".format(SRV_DIR)
    os.chdir(SRV_DIR)

    print time.asctime(), "Kotnetcli Test Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Kotnetcli Test Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

if __name__ == '__main__':
    main()
