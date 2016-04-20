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

from .browser import * 

from .communicator.error_codes import *

import logging
logger = logging.getLogger(__name__)

EXIT_FAILURE = 1 ## Tijdelijke exitcode, moet nog worden geïmplementeerd.
EXIT_SUCCESS = 0

class SuperWorker(object):
    def __init__(self, institution):
        self.browser = KotnetBrowser(institution)
    
    def check_kotnet(self, co):
        co.eventCheckNetworkConnection()
        try:
            self.browser.check_connection()
        except NetworkCheckException, e:
            co.eventFailure(KOTNETCLI_SERVER_OFFLINE)
            sys.exit(EXIT_FAILURE)
        except Exception, e:
            co.eventFailure(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

## A worker class that either succesfully logs you in to kotnet
## or exits with failure, reporting events to the given communicator
class LoginWorker(SuperWorker):
    def go(self, co, creds):
        logger.debug("enter LoginWorker.go()")
        
        self.check_kotnet(co)
        self.login_gegevensinvoeren(co)
        self.login_gegevensopsturen(co,creds)
        self.login_resultaten(co)
        
        logger.debug("LoginWorker: exiting with success")
        sys.exit(EXIT_SUCCESS)
        
    def login_gegevensinvoeren(self, co):
        co.eventGetData()
        try:
            self.browser.login_get_request()
        except Exception, e:
            co.eventFailure(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

    def login_gegevensopsturen(self, co, creds):
        co.eventPostData()
        try:
            self.browser.login_post_request(creds)
        except Exception, e:
            co.eventFailure(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

    ##TODO overwegen om meer info dan alleen maar de rccode door te geven aan
    ## eventFailure --> soort van FailureInfo object met dan bv IP address, of
    ## institution, of rccode/html dump, of stacktrace string, ...
    def login_resultaten(self, co):
        co.eventProcessData()
        try:
            tup = self.browser.login_parse_results()
            co.eventLoginSuccess(tup[0], tup[1])
        except WrongCredentialsException:
            co.eventFailure(KOTNETCLI_SERVER_WRONG_CREDS)
            sys.exit(EXIT_FAILURE)
        except MaxNumberIPException:
            co.eventFailure(KOTNETCLI_SERVER_MAX_IP)
            sys.exit(EXIT_FAILURE)
        except InvalidInstitutionException, e:
            co.eventFailure(KOTNETCLI_SERVER_INVALID_INSTITUTION)
            sys.exit(EXIT_FAILURE)
        except InternalScriptErrorException:
            co.eventFailure(KOTNETCLI_SERVER_SCRIPT_ERROR)
            sys.exit(EXIT_FAILURE)
        except UnknownRCException, e:
            co.eventFailure(KOTNETCLI_SERVER_UNKNOWN_RC)
            (rccode, html) = e.get_info()
            logger.debug("unknown rc code: {}".format(rccode))
            logger.debug("====== START HTML DUMP ======\n")
            logger.debug(html)
            logger.debug("====== END HTML DUMP ======\n")
            sys.exit(EXIT_FAILURE)
        except Exception, e:
            co.eventFailure(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

class DummyLoginWorker(LoginWorker):
    def __init__(self, inst="kuleuven", dummy_timeout=0.1, kotnet_online=True, netlogin_unavailable=False, \
        rccode=RC_LOGIN_SUCCESS, downl=44, upl=85):
        self.browser = DummyBrowser(inst, dummy_timeout, kotnet_online, netlogin_unavailable, rccode, downl, upl)
