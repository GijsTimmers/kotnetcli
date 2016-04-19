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
        co.eventKotnetVerbindingStart()
        try:
            self.browser.check_connection()
        except NetworkCheckException, e:
            co.finalize(KOTNETCLI_OFFLINE)
            sys.exit(EXIT_FAILURE)
        except Exception, e:
            co.finalize(KOTNETCLI_INTERNAL_ERROR)
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
        
        co.beeindig_sessie()
        logger.debug("LoginWorker: exiting with success")
        sys.exit(EXIT_SUCCESS)        
        
    def login_gegevensinvoeren(self, co):
        co.eventNetloginStart()
        try:
            self.browser.login_get_request()
            co.eventNetloginSuccess()
        except Exception, e:
            co.finalize(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

    def login_gegevensopsturen(self, co, creds):
        co.eventOpsturenStart()
        try:
            self.browser.login_post_request(creds)
            co.eventOpsturenSuccess()
        except Exception, e:
            co.finalize(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

    def login_resultaten(self, co):
        try:
            tup = self.browser.login_parse_results()
            co.eventLoginGeslaagd(tup[0], tup[1])
        except WrongCredentialsException:
            co.finalize(KOTNETCLI_WRONG_CREDS)
            sys.exit(EXIT_FAILURE)
        except MaxNumberIPException:
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("U bent al ingelogd op een ander IP-adres. Gebruik " + \
            "kotnetcli --force-login om u toch in te loggen.")
            sys.exit(EXIT_FAILURE)
        except InvalidInstitutionException, e:
            co.beeindig_sessie(EXIT_FAILURE)
            #TODO we could use e.get_msg() here maybe?
            logger.error("Uw gekozen institutie '%s' klopt niet. Gebruik " + \
            "kotnetcli --institution om een andere institutie te kiezen.", e.get_inst())
            sys.exit(EXIT_FAILURE)
        except InternalScriptErrorException:
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("De kotnet server rapporteert een 'internal script error'." \
                " Probeer opnieuw in te loggen...")
            sys.exit(EXIT_FAILURE)
        except UnknownRCException, e:
            co.beeindig_sessie(EXIT_FAILURE)
            (rccode, html) = e.get_info()
            logger.debug("====== START HTML DUMP ======\n")
            logger.debug(html)
            logger.debug("====== END HTML DUMP ======\n")
            logger.error("rc-code '%s' onbekend. Probeer opnieuw met de --debug optie en maak een issue aan " + \
            "(https://github.com/GijsTimmers/kotnetcli/issues/new) om ondersteuning te krijgen.", rccode)
            sys.exit(EXIT_FAILURE)
        except Exception, e:
            co.finalize(KOTNETCLI_INTERNAL_ERROR)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)        

class DummyLoginWorker(LoginWorker):
    def __init__(self, inst="kuleuven", dummy_timeout=0.1, kotnet_online=True, netlogin_unavailable=False, \
        rccode=RC_LOGIN_SUCCESS, downl=44, upl=85):
        self.browser = DummyBrowser(inst, dummy_timeout, kotnet_online, netlogin_unavailable, rccode, downl, upl)

## A worker class that either succesfull logs you off from kotnet
## or exits with failure, reporting events to the given communicator
## Do not use Kotnetlogout for integration in a forced-login method. We have
## KotnetForceLogin() for this purpose.
class LogoutWorker(SuperWorker):
    def go(self, co, creds):
        self.logout_formulieraanmaken(co, creds)
        self.logout_formulieropsturen(co)
        self.logout_resultaten(co)
    
    def logout_formulieraanmaken(self, co, creds):
        co.eventFormulierAanmakenStart()
        try:
            self.browser.logout_input_credentials(creds)
            co.eventFormulierAanmakenSuccess()
        except:
            co.eventFormulierAanmakenFailure()
            sys.exit(EXIT_FAILURE)
    
    def logout_formulieropsturen(self, co):
        co.eventFormulierOpsturenStart()
        try:
            self.browser.logout_send_credentials()
            co.eventFormulierOpsturenSuccess()
        except:
            co.eventFormulierOpsturenFailure()
            sys.exit(EXIT_FAILURE)

    def logout_resultaten(self, co):
        if logout_parse_results():
            print "success!"
        else:
            print "outch!"
        co.beeindig_sessie()

class DummyLogoutWorker(LogoutWorker):
    def __init__(self):
        self.browser = DummyBrowser()
