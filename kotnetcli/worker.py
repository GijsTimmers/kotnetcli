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

from .browser import (                  ## Doet het eigenlijke browserwerk
    KotnetBrowser,
    DummyBrowser,
    
    WrongCredentialsException,
    InternalScriptErrorException,
    InvalidInstitutionException,
    MaxNumberIPException,
    UnknownRCException,
)

import server.rccodes

#from tools import pinger                ## Om te checken of we op Kotnet zitten
#from tools import errorcodes as error   ## Om magic number errors te voorkomen

import logging
logger = logging.getLogger(__name__)

EXIT_FAILURE = 1 ## Tijdelijke exitcode, moet nog worden geïmplementeerd.
EXIT_SUCCESS = 0

class SuperWorker(object):
    def __init__(self, institution):
        self.browser = KotnetBrowser(institution)
    
    def check_kotnet(self, co):
        co.eventKotnetVerbindingStart()
        if (self.browser.bevestig_kotnetverbinding()):
            co.eventKotnetVerbindingSuccess()
        else:
            co.eventKotnetVerbindingFailure()
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("Connection attempt to {} timed out. Are you on the kotnet network?".format(self.browser.host))
            sys.exit(EXIT_FAILURE)

## A worker class that either succesfully logs you in to kotnet
## or exits with failure, reporting events to the given communicator
class LoginWorker(SuperWorker):
    def go(self, co, creds):
        logger.debug("enter LoginWorker.go()")
        
        self.check_kotnet(co)
        self.netlogin(co)
        #self.kies_kuleuven(co)
        self.login_gegevensinvoeren(co, creds)
        self.login_gegevensopsturen(co)
        self.login_resultaten(co)
        
        co.beeindig_sessie()
        logger.debug("LoginWorker: exiting with success")
        sys.exit(EXIT_SUCCESS)        
        
    def netlogin(self, co):
        co.eventNetloginStart()
        try:
            self.browser.login_open_netlogin()
            co.eventNetloginSuccess()
        except Exception, e:
            co.eventNetloginFailure()
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("fatal exception '%s' with traceback:" % e)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

#    def kies_kuleuven(self, co):
#        co.eventKuleuvenStart()
#        try:
#            self.browser.login_kies_kuleuven()
#            co.eventKuleuvenSuccess()
#        except:
#            co.eventKuleuvenFailure()
#            co.beeindig_sessie(EXIT_FAILURE)
#            sys.exit(EXIT_FAILURE)
    
    def login_gegevensinvoeren(self, co, creds):
        co.eventInvoerenStart()
        try:
            self.browser.login_input_credentials(creds)
            co.eventInvoerenSuccess()
        except Exception, e:
            co.eventInvoerenFailure()
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("fatal exception '%s' with traceback:" % e)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

    def login_gegevensopsturen(self, co):
        co.eventOpsturenStart()
        try:
            self.browser.login_send_credentials()
            co.eventOpsturenSuccess()
        except Exception, e:
            co.eventOpsturenFailure()
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("fatal exception '%s' with traceback:" % e)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

    def login_resultaten(self, co):
        try:
            tup = self.browser.login_parse_results()
            co.eventLoginGeslaagd(tup[0], tup[1])
        except WrongCredentialsException:
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("Uw logingegevens kloppen niet. Gebruik kotnetcli " + \
            "--forget om deze te resetten.")
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
            co.beeindig_sessie(EXIT_FAILURE)
            logger.error("fatal exception '%s' with traceback:" % e)
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

class DummyLoginWorker(LoginWorker):
    def __init__(self, inst="kuleuven", dummy_timeout=0.1, kotnet_online=True, netlogin_unavailable=False, \
        rccode=server.rccodes.RC_LOGIN_SUCCESS, downl=44, upl=85):
        #self.browser = DummyBrowser(inst, dummy_timeout, kotnet_online, netlogin_unavailable, rccode, downl, upl)
        self.browser = KotnetBrowser(inst, "localhost", "8000")

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

'''
class ForceerLoginWorker(LoginWorker, LogoutWorker):
    def go(self, co, creds):
        ## IP van uit te loggen apparaat opzoeken
        self.netlogin(co)
        self.kies_kuleuven(co)
        self.login_gegevensinvoeren(co, creds)
        self.login_gegevensopsturen(co)
        self.oudipophalen(co)
        ## Uitloggen
        self.logout_formulieraanmaken(co, creds)
        self.logout_formulieropsturen(co)
        self.logout_resultaten(co)
        ## re-login
        self.netlogin(co)
        self.kies_kuleuven(co)
        self.login_gegevensinvoeren(co, creds)
        self.login_gegevensopsturen(co)
        self.login_resultaten(co)
    
    def oudipophalen(self, co):
        try:
            self.browser.uitteloggenipophalen()
            co.ipophalenSucces() ## te implementeren
        except:
            co.ipophalenFailure()
            sys.exit(EXIT_FAILURE)
'''
