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

import argparse
from kotnetcli import KotnetCLI
from worker import DummyLoginWorker, DummyLogoutWorker
from communicator.fabriek import LoginCommunicatorFabriek, LogoutCommunicatorFabriek    ## Voor output op maat
from credentials import DummyCredentials     ## Opvragen van nummer en wachtwoord
from testsuite import LoginTestsuiteWorker

import browser # for RC_CODES

import logging
logger = logging.getLogger(__name__)

## a custom type checker for argparse
def positive_float(string):
    value = float(string)
    if (value < 0):
        raise argparse.ArgumentTypeError("%s is not a positive float value" % string)
    return value 

## An extended KotnetCLI to allow dummy behavior for testing purposes
class KotnetCLITester(KotnetCLI):

    def __init__(self):
        super(KotnetCLITester, self).__init__("dummy script " + \
        "om in- of uit te loggen op KotNet", log_level_default="info")
        
    def voegArgumentenToe(self, log_level_default):
        super(KotnetCLITester, self).voegArgumentenToe(log_level_default)
        
        ## override the login option to allow a user-defined rccode to be passed
        self.workergroep.add_argument("-i", "--login",
            help="Simulates a login to KotNet with a given rccode result",
            nargs="?", type=int, const=browser.RC_LOGIN_SUCCESS, metavar="RC_CODE",
            action="store", default=browser.RC_LOGIN_SUCCESS)
        
        self.workergroep.add_argument("-r", "--run-tests", \
        help="Runs a bunch of tests and assertions", action="store_true")
        
        self.parser.add_argument("--timeout", metavar="DELAY", \
        help="specify the timeout (in seconds) voor dummy browser replies", \
        type=positive_float, default=0.1)
    
    ## override with dummy behavior
    def parseActionFlags(self, argumenten):
        if argumenten.logout:
            logger.info("ik wil uitloggen voor spek en bonen")
            return (DummyLogoutWorker(), LogoutCommunicatorFabriek())
        
        elif argumenten.run_tests:
            logger.info("ik wil testen")
            return (LoginTestsuiteWorker(argumenten.institution, argumenten.timeout), \
                LoginCommunicatorFabriek())
            
        else:
            ## default option: argumenten.login
            logger.info("ik wil inloggen voor spek en bonen met RC_CODE %s",
                argumenten.login)
            return (DummyLoginWorker(argumenten.institution, argumenten.timeout, \
                True, False, argumenten.login), \
                LoginCommunicatorFabriek())
        
    def parseCredentialFlags(self, argumenten):
        logger.info("ik wil credentials ophalen voor spek en bonen")
        return self.parseCredsFlags(argumenten, DummyCredentials())

## Start de zaak asa deze file rechtstreeks aangeroepen is vanuit
## command line (i.e. niet is geimporteerd vanuit een andere file)
if  __name__ =='__main__':
    k = KotnetCLITester()
    k.parseArgumenten()
