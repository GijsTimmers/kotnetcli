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

## kotnetcli.py: encapsulates the end-user command line interface. It parses
## the command line arguments to:
##  - create the appropriate credentials instance
##  - create the appropriate communicator instance
##  - create and start the appropriate worker instance

import sys                              ## Basislib
import argparse                         ## Parst argumenten
import argcomplete                      ## Argumenten aanvullen met Tab
import logging                          ## Voor uitvoer van debug-informatie

from .communicator.fabriek import (     ## Voor output op maat
    LoginCommunicatorFabriek, 
    ForgetCommunicatorFabriek,
    inst_dict
)

from .credentials import (              ## Voor opvragen van s-nummer
    KeyRingCredentials,                 ## en wachtwoord
    GuestCredentials
)                                           
from .worker import (                   ## Stuurt alle losse componenten aan
    LoginWorker,
    ForgetCredsWorker,
    EXIT_FAILURE,
    EXIT_SUCCESS
)

from .tools import log                  ## Custom logger
from .tools import logo
from .tools import license

from __init__ import __version__, __version_str__, __src_url__

logger = logging.getLogger(__name__)

## An argument parse action that prints license information on stdout and exits
class PrintLicenceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(license.license.format(github_url=__src_url__))
        exit(0)

## An argument parse action that prints version info on stdout and exits
class PrintVersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(logo.logo.format(version=__version_str__, github_url=__src_url__))
        exit(0)

def init_debug_level(log_level, include_time):
    try:
        log.init_logging(log_level, include_time)
    except ValueError:
        print "kotnetcli: Invalid debug level: %s" % log_level
        sys.exit(1)

## TODO create an AbstractKotnetCLI class for common CLI arguments (eg version,
## license, debug level, ...) --> shared between all binaries in the kotnetcli
## distribution: kotnetcli, kotnetcli-dev, kotnetgui, kotnetcli-srv
##
## A class encapsulating the argument parsing behavior
## Note: directly inherit from "object" in order to be able to use super() in child classes
class KotnetCLI(object):
    
    ## Note: create the parser and groups as instance fiels so subclasses can access them
    ##
    ## We create three different groups, whose arguments can't be mixed (using
    ## the add_mutually_exclusive_group() option. If you enter non-combinable
    ## options, you'll get an error. To support grouping in the help messages,
    ## we add them inside an argument_group (as in http://bugs.python.org/issue10680)
    ##
    ## Then, we use "store_true" to allow elif style switching over the groups. Non-true
    ## values can be specified by using "default=False" to get "store_true" semantics.
    ## This avoids the need for complex decision trees.
    ##
    ## Finally, we call argcomplete, so that we can complete flags automatically
    ## when using bash.
    def __init__(self, descr="Script om in- of uit te loggen op KotNet", \
    log_level_default = "warning"):
        epilog_string = "return values:\n  %s\t\t\ton success\n  %s\t\t\ton failure" % (EXIT_SUCCESS, EXIT_FAILURE)
        self.parser = argparse.ArgumentParser(description=descr, epilog=epilog_string, \
            formatter_class=argparse.RawDescriptionHelpFormatter,conflict_handler='resolve')
        dummygroup = self.parser.add_argument_group("worker options")
        self.workergroep = dummygroup.add_mutually_exclusive_group()
        dummygroup = self.parser.add_argument_group("credentials options")
        self.credentialsgroep = dummygroup.add_mutually_exclusive_group()
        dummygroup = self.parser.add_argument_group("communicator options")
        self.communicatorgroep = dummygroup.add_mutually_exclusive_group()
        self.voegArgumentenToe(log_level_default)
        argcomplete.autocomplete(self.parser)
    
    def voegArgumentenToe(self, log_level_default):
        ########## general flags ##########
        self.parser.add_argument("-v", "--version", action=PrintVersionAction, \
        help="show program's version number and exit", nargs=0)
        self.parser.add_argument("-l", "--license", action=PrintLicenceAction, \
        help="show license info and exit", nargs=0)
        ## debug flag with optional (nargs=?) level; defaults to LOG_LEVEL_DEFAULT if
        ## option not present; defaults to debug if option present but no level specified
        self.parser.add_argument("--debug", help="specify the debug verbosity", \
            nargs="?", const="debug", metavar="LEVEL",
            choices=[ 'critical', 'error', 'warning', 'info', 'debug' ],
            action="store", default=log_level_default)

        self.parser.add_argument("--time", action="store_true", \
            help="include fine-grained timing info in logger output")
        
        self.parser.add_argument("--institution", help="override the instititution", \
            metavar="INST", action="store", default=None,
            choices=inst_dict.keys())
        
        ########## login type flags ##########
        self.workergroep.add_argument("-i", "--login",\
        help="Logs you in on KotNet (default)", action="store_true")
        
        self.workergroep.add_argument("-o", "--logout",\
        help="Logs you out off KotNet", action="store_true")
        
        self.workergroep.add_argument("-f", "--forget",\
        help="Makes kotnetcli forget your credentials",\
        action="store_true")
        
        ########## credentials type flags ##########
        self.credentialsgroep.add_argument("-k", "--keyring",\
        help="Makes kotnetcli pick up your credentials from the keyring (default)",\
        action="store_true")
        
        self.credentialsgroep.add_argument("-g", "--guest-mode",\
        help="Logs you in as a different user without forgetting your \
        default credentials", action="store_true")
        
        ########## communicator flags ##########
        self.communicatorgroep.add_argument("-t", "--plaintext",\
        help="Logs you in using plaintext output",\
        action="store_const", dest="communicator", const="plaintext")

        ## nargs=3 to allow a user to supply optional colorname arguments
        ## default=False to get "store_true" semantics when option not specified
        self.communicatorgroep.add_argument("-c", "--color",\
        help="Logs you in using custom colors", \
        action="store_const", dest="communicator", const="colorama" )
        
        self.communicatorgroep.add_argument("-d", "--dialog",\
        help="Omits the curses interface by using dialog based output",\
        action="store_const", dest="communicator", const="dialog")

        self.communicatorgroep.add_argument("-l", "--logger",\
        help="Reports progress through the logging module",\
        action="store_const", dest="communicator", const="logger")
        
        self.communicatorgroep.add_argument("-s", "--summary",\
        help="Hides all output except for a short summary",\
        action="store_const", dest="communicator", const="summary")
        
        self.communicatorgroep.add_argument("-q", "--quiet",\
        help="Hides all output",\
        action="store_const", dest="communicator", const="quiet")
                
    ## Parses the arguments corresponding to self.parser
    def parseArgumenten(self):
        argumenten = self.parser.parse_args()
        ## 0. general flags
        init_debug_level(argumenten.debug, argumenten.time)
        logger.debug("parse_args() is: %s", argumenten)
        ## 1. credential-related flags
        creds = self.parseCredentialFlags(argumenten)
        ## 2. login-type flags
        (worker, fabriek) = self.parseActionFlags(argumenten)
        ## 3. communicator-related flags
        try:
            co = self.parseCommunicatorFlags(fabriek, argumenten)
        except ImportError, e:
            logger.error(
                "import error when trying to create '%s' communicator: %s\n"    \
                "Have you installed all the dependencies?\n"                    \
                "See also <%s/wiki/Dependencies-overview>",
                argumenten.communicator, e, GITHUB_URL)
            sys.exit(EXIT_FAILURE)
        ## 4. start the process
        worker.go(co, creds)

    ## returns newly created credentials obj
    def parseCredentialFlags(self, argumenten):
        if argumenten.guest_mode:
            logger.info("ik wil me anders voordoen dan ik ben")
            return GuestCredentials(argumenten.institution)
        else:
            logger.info("ik haal de credentials uit de keyring")
            return KeyRingCredentials(argumenten.institution)

    ## returns tuple (worker, fabriek)
    def parseActionFlags(self, argumenten):
        if argumenten.forget:
            logger.info("ik wil vergeten")
            worker = ForgetCredsWorker()
            fabriek = ForgetCommunicatorFabriek()
        elif argumenten.logout:
            logger.info("ik wil uitloggen")
            raise NotImplementedError
        else:
            ## default option: argumenten.login
            logger.info("ik wil inloggen")
            worker = LoginWorker(argumenten.institution)
            fabriek = LoginCommunicatorFabriek()

        return (worker, fabriek)
    
    ## returns communicator
    def parseCommunicatorFlags(self, fabriek, argumenten):
        if argumenten.communicator == "quiet":
            logger.info("ik wil zwijgen")
            return fabriek.createQuietCommunicator()
        
        if argumenten.communicator == "plaintext":
            logger.info("ik wil terug naar de basis")
            return fabriek.createPlaintextCommunicator()
        
        if argumenten.communicator == "dialog":
            logger.info("ik wil praten")
            return fabriek.createDialogCommunicator()
        
        if argumenten.communicator == "logger":
            logger.info("ik wil loggen")
            return fabriek.createLoggerCommunicator()
        
        if argumenten.communicator == "summary":
            logger.info("ik wil het mooie in de kleine dingen zien")
            return fabriek.createSummaryCommunicator()
        
        else:
            ## default option: argumenten.color with default colors
            logger.info("ik ga mee met de stroom")
            argumenten.communicator = "colorama"
            return fabriek.createColoramaCommunicator()
        
## end class KotnetCLI

## main()-functie:
## - aangrijpingspunt kotnetcli-runner.py
## - aangrijpingspunt console_script van setup.py
def main():
    try:
        k = KotnetCLI()
        k.parseArgumenten()
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt received")
        sys.exit(EXIT_FAILURE)
