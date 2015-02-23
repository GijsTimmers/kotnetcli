#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To  view a copy of
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View,
## CA 94042, USA.

## kotnetcli_test.py: an extension of kotnetcli.py, containing some
## extra developer/debug related command line options

import argparse
from kotnetcli import KotnetCLI
from worker import DummyLoginWorker, DummyLogoutWorker
from communicator.fabriek import LoginCommunicatorFabriek, LogoutCommunicatorFabriek    ## Voor output op maat
from credentials import DummyCredentials     ## Opvragen van nummer en wachtwoord
from testsuite import LoginTestsuiteWorker

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
        
        self.parser.add_argument("-r", "--run-tests", \
        help="Run a bunch of tests and assertions", action="store_true")
        
        self.parser.add_argument("--timeout", metavar="DELAY", \
        help="Specify the timeout (in seconds) voor dummy browser replies", \
        type=positive_float, default=0.1)
    
    ## override with dummy behavior
    def parseActionFlags(self, argumenten):
        if argumenten.logout:
            logger.info("ik wil uitloggen voor spek en bonen")
            return (DummyLogoutWorker(), LogoutCommunicatorFabriek())
        
        elif argumenten.run_tests:
            logger.info("ik wil testen")
            return (LoginTestsuiteWorker(argumenten.timeout), \
                LoginCommunicatorFabriek())
            
        else:
            ## default option: argumenten.login
            logger.info("ik wil inloggen voor spek en bonen")
            return (DummyLoginWorker(argumenten.timeout), \
                LoginCommunicatorFabriek())
        
    def parseCredentialFlags(self, argumenten):
        logger.info("ik wil credentials ophalen voor spek en bonen")
        return self.parseCredsFlags(argumenten, DummyCredentials())

## Start de zaak asa deze file rechtstreeks aangeroepen is vanuit
## command line (i.e. niet is geimporteerd vanuit een andere file)
if  __name__ =='__main__':
    k = KotnetCLITester()
    k.parseArgumenten()
