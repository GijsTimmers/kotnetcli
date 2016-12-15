#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import requests                         ## Invullen van HTTP POST-request
import socket                           ## Voor ophalen IP

from bs4 import BeautifulSoup, Comment  ## Om webinhoud proper te parsen.

## login rc codes contained in the response html page
from server.rccodes import *

import logging
logger = logging.getLogger(__name__)

from __init__ import resolve_path

NETLOGIN_HOST       = "netlogin.kuleuven.be"
NETLOGIN_PORT       = 443

LOCALHOST           = "localhost"
LOCALHOST_PORT      = "8888"

## the maximum waiting time in seconds for browser connections
BROWSER_TIMEOUT_SEC = 1.5

## custom exceptions to be caught by worker
class KotnetOfflineException(Exception):
    pass

class WrongCredentialsException(Exception):
    pass

class InternalScriptErrorException(Exception):
    pass

class InvalidInstitutionException(Exception):
    pass
    
class MaxNumberIPException(Exception):
    pass
    
class UnknownRCException(Exception):
    def __init__(self, rccode, html):
        self.rccode = rccode
        self.html = html

    def get_info(self):
        return (self.rccode, self.html)

## The class doing the actual browser emulation work.
## KotnetBrowser() is like an API: it contains all possible Browser operations.
## So, we don't create a LoginBrowser(), LogoutBrowser(), etc. Instead, the
## proper Worker() is instantiated by kotnetcli.py, and this instance calls
## only the Browser() methods that it needs.
class KotnetBrowser(object):
     
    ## Note: the browser itself doesn't save any credentials. These are kept in a
    ## credentials object that is supplied when needed
    def __init__(self, localhost=False):
        self.language = "nl"
        self.host = NETLOGIN_HOST if not localhost else LOCALHOST
        self.port = NETLOGIN_PORT if not localhost else LOCALHOST_PORT
        self.protocol = "https" if not localhost else "http"

    def get_server_url(self):
        return "{}://{}:{}".format(self.protocol, self.host, self.port)
        
    def check_connection(self):
        try:
            sock = socket.create_connection((self.host, self.port),
                                                BROWSER_TIMEOUT_SEC)
            sock.close()
        except socket.error:
            raise KotnetOfflineException
    
    def do_server_request(self, method, cgi_script, params=None, data=None):
        url = self.get_server_url() + "/cgi-bin/{}".format(cgi_script)
        try:
            r = requests.request(method, url, verify=True, params=params,
                                    data=data, timeout=BROWSER_TIMEOUT_SEC)
        except requests.exceptions.Timeout:
            raise KotnetOfflineException
        logger.debug("server HTTP '{}' response status code is {}".format(
                                    method, r.status_code))
        return r.text
    
    def login_get_request(self, creds):
        payload = {
            "inst"      : creds.getInst(),
            "lang"      : self.language,
            "submit"    : "Ga verder / Continue",
        }
        html = self.do_server_request('GET', 'wayf2.pl', params=payload)
        ## search for something of the form name="pwd123" and extract the pwd123 part
        self.wachtwoordvak = re.findall("(?<=name=\")pwd\d*", html)[0]
        
    def login_post_request(self, creds):
        payload = {
            "inst"              : creds.getInst(),
            "lang"              : self.language,
            "submit"            : "Login",
            "uid"               : creds.getUser(),
            self.wachtwoordvak  : creds.getPwd()
        }
        self.html = self.do_server_request('POST', 'netlogin.pl', data=payload)
        logger.debug("Server reply for HTML POST is:\n" + self.html)

    ## This method parses the server's response. On success, it returns a tuple of
    ## length 2: (downloadpercentage, uploadpercentage); else it raises an
    ## appropriate exception
    def login_parse_results(self):
        #soup = BeautifulSoup(self.html, "lxml")
        soup = BeautifulSoup(self.html, "html.parser")   
        ## Zoek naar de rc-code in de comments van het html-bestand. Deze
        ## bevat de status.
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        p = re.compile("weblogin: rc=\d+")
        for c in comments:
            m = p.search(c)
            #m = p.findall(c)
            #print m
            if m:
                rccode = int(m.group().strip("weblogin: rc="))
                ## m = p.search(c): zoekt naar de RE p in c. Indien die is
                ## gevonden, is m een object; m.group() geeft vervolgens
                ## weer waar de RE matcht. Dit doet het maar één keer; als
                ## je strings op meerdere matches wilt controleren, moet je
                ## p.findall(c) gebruiken, zoals hieronder.

        logger.debug("rccode is %s", rccode)

        if rccode == RC_LOGIN_SUCCESS:
            ## downloadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[6])
            downloadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            ## uploadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[7])
            uploadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            return (downloadpercentage, uploadpercentage)

        elif (rccode == RC_LOGIN_INVALID_USERNAME) or \
            (rccode == RC_LOGIN_INVALID_PASSWORD):
            raise WrongCredentialsException()
            
        elif rccode == RC_LOGIN_MAX_IP:
            raise MaxNumberIPException()

        elif rccode == RC_INVALID_INSTITUTION:
            raise InvalidInstitutionException()
        
        elif self.rccode == RC_INTERNAL_SCRIPT_ERR:
            raise InternalScriptErrorException()

        else:
            raise UnknownRCException(rccode, self.html)
