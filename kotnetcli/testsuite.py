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

from worker import DummyLoginWorker, SuperWorker, EXIT_SUCCESS, EXIT_FAILURE
import browser

import logging
logger = logging.getLogger(__name__)

##TODO deprecated: remove
class LoginTestsuiteWorker(SuperWorker):

    def __init__(self, inst, dummy_browser_timeout):
        self.inst = inst
        self.timeout = dummy_browser_timeout

    def go(self, co, creds):
        logger.info("running dummy login testsuite with communicator '%s' and " \
        "timeout %s for inst '%s'\n", co.__class__.__name__, self.timeout, self.inst)
        self.run_dummy_login_tests(co, creds)
        logger.info("end of dummy login testsuite with communicator " + \
        "'%s'", co.__class__.__name__)
        exit(0)
    
    ## TODO assert for the correct fine grained exit code here (see corresponding issue)
    def run_dummy_login_tests(self, co, creds):
    
        logger.info("DEFAULT DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout)
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_SUCCESS)
            logger.info("DEFAULT DUMMY LOGIN END\n")
        
        logger.info("LOW PERCENTAGES DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, browser.RC_LOGIN_SUCCESS, -5, 22.5)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_SUCCESS)
            logger.info("LOW PERCENTAGES DUMMY LOGIN END\n")
        
        logger.info("KOTNET OFFLINE DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, False) 
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("KOTNET OFFLINE DUMMY LOGIN END\n")
        
        logger.info("NETLOGIN OFFLINE DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, True)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("NETLOGIN OFFLINE DUMMY LOGIN END\n")
        
        logger.info("INVALID USERNAME DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, browser.RC_LOGIN_INVALID_USERNAME)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("INVALID USERNAME DUMMY LOGIN END\n")
        
        logger.info("INTERNAL SCRIPT ERROR LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, browser.RC_INTERNAL_SCRIPT_ERR)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("INTERNAL SCRIPT ERROR LOGIN END\n")
        
        logger.info("INVALID PASSWORD DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, browser.RC_LOGIN_INVALID_PASSWORD)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("INVALID PASSWORD DUMMY LOGIN END\n")
        
        logger.info("MAX IP DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, browser.RC_LOGIN_MAX_IP)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("MAX IP DUMMY LOGIN END\n")
        
        logger.info("UNKNOWN INSTITUTION DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, browser.RC_INVALID_INSTITUTION)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("UNKNOWN INSTITUTION DUMMY LOGIN END\n")

        logger.info("UNKNOWN RC (DEBUG ON) DUMMY LOGIN START")
        co.__init__()
        worker = DummyLoginWorker(self.inst, self.timeout, True, False, 300)
        worker_logger = logging.getLogger("worker")
        worker_logger.setLevel(logging.DEBUG)
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("UNKNOWN RC (DEBUG ON) DUMMY LOGIN END\n")        
        
        logger.info("UNKNOWN RC (DEBUG OFF) DUMMY LOGIN START")
        co.__init__()
        worker_logger.setLevel(logging.WARNING)
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("UNKNOWN RC (DEBUG OFF) DUMMY LOGIN END\n")
        
## end class LoginTestsuiteWorker
