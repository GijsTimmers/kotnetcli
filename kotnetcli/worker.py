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

## worker.py: directs the login/logout process:
##  - receives a 'black box' credentials and communicator instance
##  - uses the KotnetBrowser interface to do the actual actions one
##    after the other, in the correct order
##  - sends status updates to the communicator
##  - exits with the corresponding exit code

import sys                              ## Basislib
import traceback

from .credentials import ForgetCredsException
from .browser import *

import logging
logger = logging.getLogger(__name__)

EXIT_FAILURE = 1 ## Tijdelijke exitcode, moet nog worden geïmplementeerd.
EXIT_SUCCESS = 0

class AbstractWorker(object):
    def go(self, co, creds):
        try:
            logger.debug("Enter worker.go()")
            self.do_work(co, creds)
            logger.debug("Exiting worker with success")
            sys.exit(EXIT_SUCCESS)
        ## fail gracefully when encountering an unexpected error
        except Exception:
            logger.debug("Caught worker exception; exiting with failure")
            co.eventFailureInternalError(traceback.format_exc())
            sys.exit(EXIT_FAILURE)

class ForgetCredsWorker(AbstractWorker):
    def do_work(self, co, creds):
        try:
            co.eventForgetCreds()
            creds.forgetCreds()
            co.eventForgetCredsSuccess()
        except ForgetCredsException:
            co.eventFailureForget()
            sys.exit(EXIT_FAILURE)

class SuperNetworkWorker(AbstractWorker):
    def __init__(self, localhost=False):
        self.browser = KotnetBrowser(localhost)
    
    def check_credentials(self, co, creds):
        if not creds.hasCreds():
            logger.info("querying for user credentials")
            try:
                (username, pwd, inst) = co.eventPromptCredentials()
            except Exception:
                ## fail gracefully for a communicator input failure
                logger.warning("communicator prompt exception; exiting with failure")
                logger.debug(traceback.format_exc())
                sys.exit(EXIT_FAILURE)
            creds.storeCreds(username, pwd, inst)
        logger.debug("got creds for user %s@%s", creds.getUser(), creds.getInst())
    
    def contact_server(self, co, fct, *args):
        try:
            fct(*args)
        except KotnetOfflineException:
            co.eventFailureOffline(self.browser.get_server_url())
            sys.exit(EXIT_FAILURE)
    
    def check_kotnet(self, co):
        co.eventCheckNetworkConnection()
        self.contact_server(co, self.browser.check_connection)

## A worker class that either succesfully logs you in to kotnet
## or exits with failure, reporting events to the given communicator
class LoginWorker(SuperNetworkWorker):
    def do_work(self, co, creds):
        self.check_credentials(co,creds)
        self.check_kotnet(co)
        self.login_gegevensinvoeren(co, creds)
        self.login_gegevensopsturen(co, creds)
        self.login_resultaten(co, creds)
        
    def login_gegevensinvoeren(self, co, creds):
        co.eventGetData()
        self.contact_server(co, self.browser.login_get_request, creds)

    def login_gegevensopsturen(self, co, creds):
        co.eventPostData()
        self.contact_server(co, self.browser.login_post_request, creds)

    def login_resultaten(self, co, creds):
        co.eventProcessData()
        try:
            tup = self.browser.login_parse_results()
            co.eventLoginSuccess(tup[0], tup[1])
        except WrongCredentialsException:
            co.eventFailureCredentials()
            sys.exit(EXIT_FAILURE)
        except MaxNumberIPException:
            co.eventFailureMaxIP()
            sys.exit(EXIT_FAILURE)
        except InvalidInstitutionException, e:
            co.eventFailureInstitution(creds.getInst())
            sys.exit(EXIT_FAILURE)
        except InternalScriptErrorException:
            co.eventFailureServerScriptError()
            sys.exit(EXIT_FAILURE)
        except UnknownRCException, e:
            (rccode, html) = e.get_info()
            co.eventFailureUnknownRC(rccode, html)
            sys.exit(EXIT_FAILURE)

class LogoutWorker(SuperNetworkWorker):
    pass
