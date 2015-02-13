#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  https://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit https://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import argparse
from worker import DummyLoginWorker, DummyLogoutWorker, EXIT_SUCCESS, EXIT_FAILURE
from communicator.fabriek import LoginCommunicatorFabriek, LogoutCommunicatorFabriek    ## Voor output op maat
from credentials import DummyCredentials     ## Opvragen van nummer en wachtwoord

import logging
logger = logging.getLogger(__name__)


## TODO assert for the correct fine grained exit code here (see corresponding issue)
class RunTestsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        creds = DummyCredentials()
        fab = LoginCommunicatorFabriek()
        co = fab.createColoramaCommunicator()      ## change this line to test another communicator
        #co = fab.createPlaintextCommunicator()
        self.run_login_tests(co, creds)
        
        exit(0)
    
    def run_login_tests(self, co, creds):
        print "\n====== DEFAULT DUMMY LOGIN START ======"
        worker = DummyLoginWorker()
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_SUCCESS)
            print "====== DEFAULT DUMMY LOGIN END ======"
        
        print "\n====== LOW PERCENTAGES DUMMY LOGIN START ======"
        worker = DummyLoginWorker(True, False, 100, -5, 22.5)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_SUCCESS)
            print "====== LOW PERCENTAGES DUMMY LOGIN END ======"
        
        print "\n====== KOTNET OFFLINE DUMMY LOGIN START ======"
        worker = DummyLoginWorker(False)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            print "====== KOTNET OFFLINE DUMMY LOGIN END ======"
        
        print "\n====== NETLOGIN OFFLINE DUMMY LOGIN START ======"
        worker = DummyLoginWorker(True, True)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            print "====== NETLOGIN OFFLINE DUMMY LOGIN END ======"
        
        print "\n====== INVALID USERNAME DUMMY LOGIN START ======"
        worker = DummyLoginWorker(True, False, 201)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            print "====== INVALID USERNAME DUMMY LOGIN END ======"
        
        print "\n====== INVALID PASSWORD DUMMY LOGIN START ======"
        worker = DummyLoginWorker(True, False, 202)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            print "====== INVALID PASSWORD DUMMY LOGIN END ======"
        
        print "\n====== MAX IP DUMMY LOGIN START ======"
        worker = DummyLoginWorker(True, False, 206)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            print "====== MAX IP DUMMY LOGIN END ======"
        
        print "\n====== UNKOWN RC DUMMY LOGIN START ======"
        worker = DummyLoginWorker(True, False, 300)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            print "====== UNKNOWN RC DUMMY LOGIN END ======"


## end class RunTestsAction
