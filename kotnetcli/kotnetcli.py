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
import getpass                          ## Voor invoer wachtwoord zonder print
import argparse                         ## Parst argumenten
import argcomplete                      ## Argumenten aanvullen met Tab
import logging                          ## Voor uitvoer van debug-informatie

from .communicator.fabriek import (     ## Voor output op maat
    LoginCommunicatorFabriek, 
    LogoutCommunicatorFabriek           
)

from .credentials import (              ## Voor opvragen van s-nummer
    KeyRingCredentials,                 ## en wachtwoord
    ForgetCredsException
)                                           
from .worker import (                   ## Stuurt alle losse componenten aan
    LoginWorker,
    LogoutWorker,
    EXIT_FAILURE,
    EXIT_SUCCESS
)

from .tools import log                  ## Custom logger
from .tools import logo
from .tools import license

logger = logging.getLogger(__name__)

GITHUB_URL = "https://github.com/GijsTimmers/kotnetcli"

## Hardcode the version. Development versions should be suffixed with -dev;
## release versions should be followed with "Name" as well. Some examples:
## __version__ = '1.2.1 "American Craftsman"'   (A release)
## __version__ = '1.2.1-dev'                    (A development version)
__version__ = '1.3.0-dev'

## An argument parse action that prints license information on stdout and exits
class PrintLicenceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(license.license.format(github_url=GITHUB_URL))
        exit(0)

## An argument parse action that prints version info on stdout and exits
class PrintVersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(logo.logo.format(version=__version__, github_url=GITHUB_URL))
        exit(0)

def init_debug_level(log_level, include_time):
    try:
        log.init_logging(log_level, include_time)
    except ValueError:
        print "kotnetcli: Invalid debug level: %s" % log_level
        sys.exit(1)
        
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
        
        self.parser.add_argument("--institution", help="specify the instititution", \
            nargs="?", const="kuleuven", metavar="INST",
            choices=["kuleuven", "kotnetext", "kuleuven-campusnet"],
            action="store", default="kuleuven")
        
        ########## login type flags ##########
        self.workergroep.add_argument("-i", "--login",\
        help="Logs you in on KotNet (default)", action="store_true")
        
        self.workergroep.add_argument("-o", "--logout",\
        help="Logs you out off KotNet", action="store_true")
        
        '''
        self.workergroep.add_argument("-!", "--force-login",\
        help="Logs you out on other IP's, and then in on this one",\
        action="store_const", dest="worker", const="force_login")
        '''
        
        ########## credentials type flags ##########
        self.credentialsgroep.add_argument("-k", "--keyring",\
        help="Makes kotnetcli pick up your credentials from the keyring (default)",\
        action="store_true")
        
        self.credentialsgroep.add_argument("-f", "--forget",\
        help="Makes kotnetcli forget your credentials",\
        action="store_true")
        
        self.credentialsgroep.add_argument("-g", "--guest-mode",\
        help="Logs you in as a different user without forgetting your \
        default credentials", action="store_true")
        
        ########## communicator flags ##########
        self.communicatorgroep.add_argument("-t", "--plaintext",\
        help="Logs you in using plaintext output",\
        action="store_true")

        ## nargs=3 to allow a user to supply optional colorname arguments
        ## default=False to get "store_true" semantics when option not specified
        self.communicatorgroep.add_argument("-c", "--color",\
        help="Logs you in using custom colors; sequence = ok_color, wait_color, err_color, style; choices = black, red, green, yelow, blue, magenta, cyan, white",\
        choices= ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "bright", "normal"],
        nargs=4, default=False, metavar="COL")
        
        self.communicatorgroep.add_argument("-q", "--quiet",\
        help="Hides all output",\
        action="store_const", dest="communicator", const="quiet")
                
        ## voorlopig andere communicators uitschakelen in de dev branch
        """        
        self.communicatorgroep.add_argument("-u", "--curses",\
        help="Logs you in using curses output",\
        action="store_const", dest="communicator", const="curses")
        
        self.communicatorgroep.add_argument("-d", "--dialog",\
        help="Omits the curses interface by using dialog based output",\
        action="store_const", dest="communicator", const="dialog")
        
        self.communicatorgroep.add_argument("-b", "--bubble",\
        help="Hides all output except for a bubble notification",\
        action="store_const", dest="communicator", const="bubble")
        
        self.communicatorgroep.add_argument("-s", "--summary",\
        help="Hides all output except for a short summary",\
        action="store_const", dest="communicator", const="summary")
        
        self.communicatorgroep.add_argument("-q", "--quiet",\
        help="Hides all output",\
        action="store_const", dest="communicator", const="quiet")
        """
    
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
        co = self.parseCommunicatorFlags(fabriek, argumenten)
        ## 4. start the process
        worker.go(co, creds)

    ## returns newly created credentials obj
    def parseCredentialFlags(self, argumenten):
        logger.info("ik haal de credentials uit de keyring")
        return self.parseCredsFlags(argumenten, KeyRingCredentials())
    
    ## a helper method with a default credentials object argument
    def parseCredsFlags(self, argumenten, cr):
        if argumenten.forget:
            logger.info("ik wil vergeten")
            try:
                cr.forgetCreds()
                print "You have succesfully removed your kotnetcli credentials."
                sys.exit(0)
            except ForgetCredsException:
                print "You have already removed your kotnetcli credentials."
                sys.exit(1)
        
        elif argumenten.guest_mode:
            logger.info("ik wil me anders voordoen dan ik ben")
            (gebruikersnaam, wachtwoord) = self.prompt_user_creds()
            cr.saveGuestCreds(gebruikersnaam, wachtwoord)
            return cr
            
        else:
            ## default option: argumenten.keyring
            if (not cr.hasCreds()):
                (gebruikersnaam, wachtwoord) = self.prompt_user_creds()
                cr.saveCreds(gebruikersnaam, wachtwoord)
            return cr
            
    def prompt_user_creds(self):
        gebruikersnaam = raw_input("Voer uw s-nummer/r-nummer in... ")
        wachtwoord = getpass.getpass(prompt="Voer uw wachtwoord in... ")
        return (gebruikersnaam, wachtwoord)

    ## returns tuple (worker, fabriek)
    def parseActionFlags(self, argumenten):
        if argumenten.logout:
            logger.info("ik wil uitloggen")
            worker = LogoutWorker(argumenten.institution)
            fabriek = LogoutCommunicatorFabriek()
        else:
            ## default option: argumenten.login
            logger.info("ik wil inloggen")
            worker = LoginWorker(argumenten.institution)
            fabriek = LoginCommunicatorFabriek()
                
        '''elif argumenten.worker == "force_login":
            print "ik moet en zal inloggen"
            worker = ForceLoginWorker()
            fabriek = LoginCommunicatorFabriek()
        '''
        
        return (worker, fabriek)
    
    ## returns communicator
    def parseCommunicatorFlags(self, fabriek, argumenten):
        if argumenten.communicator == "quiet":
            logger.info("ik wil zwijgen")
            return fabriek.createQuietCommunicator()
        
        if argumenten.plaintext:
            logger.info("ik wil terug naar de basis")
            return fabriek.createPlaintextCommunicator()
        
        elif argumenten.color:
            logger.info("ik wil vrolijke custom kleuren: %s", argumenten.color)
            return fabriek.createColoramaCommunicator(argumenten.color)
        
        else:
            ## default option: argumenten.color with default colors
            logger.info("ik ga mee met de stroom")
            return fabriek.createColoramaCommunicator()
        
        '''
        elif argumenten.communicator == "summary":
            print "ik wil het mooie in de kleine dingen zien"
            return fabriek.createSummaryCommunicator()
        
        elif argumenten.communicator == "quiet":
            print "ik wil zwijgen"
            return fabriek.createQuietCommunicator()
        else:
            print "we still have to fix the others...."
        
        if argumenten.communicator == "curses":
            print "ik wil vloeken"
            if os.name == "posix":
                co = communicator.CursesCommunicator()
            else:
                co = communicator.ColoramaCommunicator()
        
        elif argumenten.communicator == "android":
            print "ik wou dat ik een robot was"
            co = communicator.AndroidCommunicator()
        
        elif argumenten.communicator == "colortext":
            print "ik wil vrolijke kleuren"
            ## jo: TODO changed next line in order to be able to test; should use fac here
                    
            fab = fabriek.LoginCommunicatorFabriek()
            co = fab.createColoramaCommunicator()
            ## Moet worden vervangen in de toekomst: fab moet al aangemaakt zijn
            ## door de login/logout-switch.
        
        elif argumenten.communicator == "plaintext":
            print "ik wil terug naar de basis"
            co = communicator.LogoutPlaintextCommunicator()
        
        elif argumenten.communicator == "dialog":
            print "ik wil fancy dialogs"
            if os.name == "posix":
                co = communicator.DialogCommunicator()
            else:
                co = communicator.ColoramaCommunicator()
        
        elif argumenten.communicator == "bubble":
            print "ik wil bellen blazen"
            if os.name == "posix":
                co = communicator.BubbleCommunicator()
            else:
                co = communicator.ColoramaCommunicator()
        
        elif argumenten.communicator == "summary":
            print "ik wil het mooie in de kleine dingen zien"
            co = communicator.SummaryCommunicator()
        
        elif argumenten.communicator == "quiet":
            print "ik wil zwijgen"
            co = communicator.QuietCommunicator()
        '''
## end class KotnetCLI

## main()-functie:
## - aangrijpingspunt kotnetcli-runner.py
## - aangrijpingspunt console_script van setup.py
def main():
    k = KotnetCLI()
    k.parseArgumenten()
