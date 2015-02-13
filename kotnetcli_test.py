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

class RunTestsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print "not yet implemented"
        exit(0)

## An extended KotnetCLI to allow dummy behavior for testing purposes
class KotnetCLITester(KotnetCLI):

    def __init__(self):
        super(KotnetCLITester, self).__init__("[DUMMY] script \
        om in- of uit te loggen op KotNet")

    def voegArgumentenToe(self):
        super(KotnetCLITester, self).voegArgumentenToe()
        
        self.parser.add_argument("-r", "--run-tests", \
        help="Run a bunch of tests", action=RunTestsAction, nargs=0)
    
    ## override with dummy behavior
    def parseActionFlags(self, argumenten):
        if argumenten.worker == "login":
            print "ik wil inloggen voor spek en bonen"
            worker = DummyLoginWorker()
            fabriek = LoginCommunicatorFabriek()
            
        elif argumenten.worker == "logout":
            print "ik wil uitloggen voor spek en bonen"
            worker = DummyLogoutWorker()
            fabriek = LogoutCommunicatorFabriek()
        
        return (worker, fabriek)
        
    def parseCredentialFlags(self, argumenten):
        print "ik wil credentials ophalen voor spek en bonen"
        return self.parseCredsFlags(argumenten, DummyCredentials())

## Start de zaak asa deze file rechtstreeks aangeroepen is vanuit
## command line (i.e. niet is geimporteerd vanuit een andere file)
if  __name__ =='__main__':
    print "== kotnetcli_dev started =="
    k = KotnetCLITester()
    k.parseArgumenten()
    print "== kotnetcli_dev done =="
