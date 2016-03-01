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

## declare some constants
LOG_LEVEL = "warning"
TIMEOUT = 3

## import back-end stuff
from worker import LoginWorker, EXIT_FAILURE
from credentials import KeyRingCredentials
from communicator.fabriek import LoginCommunicatorFabriek

import sys
import time
import traceback

## init logging
from tools import log
log.init_logging(LOG_LEVEL)
import logging
logger = logging.getLogger(__name__)

## Start de zaak asa deze file rechtstreeks aangeroepen is vanuit
## command line (i.e. niet is geimporteerd vanuit een andere file)
if  __name__ =='__main__':
    logger.info("starting in main")
    
    ## create necessary back-end objects
    fab = LoginCommunicatorFabriek()
    co = fab.createColoramaCommunicator()
    creds = KeyRingCredentials()
    worker = LoginWorker()
    
    ## execute login
    logger.debug("now trying worker.go()")
    try:
        worker.go(co, creds)
    except SystemExit, e:
        logger.debug("caught SystemExit with code %s" % e.code)
        exit_code = e.code
    except Exception, e:
        logger.error("something unexpected went wrong when logging in;" + \
        'exception is: "%s"\n' % e + "\tpost an issue on " + \
        "(https://github.com/GijsTimmers/kotnetcli/issues/new) to get support")
        logger.debug("exception traceback is:\n%s" % traceback.format_exc())
        exit_code = EXIT_FAILURE
    
    ## timeout and exit
    logger.info("now waiting %s seconds" % TIMEOUT)
    time.sleep(TIMEOUT)
    logger.debug("now exiting with code %s" % exit_code)
    sys.exit(exit_code)
    
