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

#import re                               ## Basislib voor reguliere expressies
#import time                             ## Voor timeout om venster te sluiten
import sys                              ## Basislib
#import os                               ## Basislib
#import platform                         ## Om onderscheid Lin/Mac te maken
from plaintextc import (
                        SuperPlaintextCommunicator,
                        LoginPlaintextCommunicator,
                        LogoutPlaintextCommunicator
                        )
#from ..tools import cursor              ## Om cursor te verbergen/tonen
from tools import cursor                ## Om cursor te verbergen/tonen

#from kotnetcli import logger
import logging
logger = logging.getLogger(__name__)

## Gijs:
## We hoeven geen relatieve import te gebruiken omdat de map waarin 
## kotnetcli.py zich bevindt de rootmap ($PYTHONPATH) is. De map 'tools'
## bevindt zich daar ook; daarom hoeven we niet te verwijzen naar de lokatie
## ten opzichte van deze specifieke communicator (denk ik)


try:            
    logger.debug("Probeert Colorama te importeren..."),
    from colorama import (              ## Voor gekleurde tekst.
                          Fore,
                          Style,
                          init as colorama_init
                          )
    logger.debug("OK")
except ImportError:
    logger.error("Couldn't import the colorama library.")
    exit(1)

class SuperColoramaCommunicator(SuperPlaintextCommunicator):
    ## I changed the structure: it used to be:
    ## SuperColoramaCommunicator(QuietCommunicator)
    ## LoginColoramaCommunicator(SuperColoramaCommunicator, LoginPlaintextCommunicator)
    ## 
    ## This caused a quiet print. See: https://github.com/GijsTimmers/kotnetcli/issues/56.
    ##
    ## Solution:
    ## Let the superclass inherit directly from LoginPlaintextCommunicator.
    ##
    ## Challenge:
    ## Make sure that LoginColoramaCommunicator inherits LoginPlaintextCommunicator
    ## and LogoutColoramaCommunicator inherits LogoutPlaintextCommunicator
    ##
    ## TODO: jo: veranderd naar single inheritance van plaintext in de super
    ## en multiple inheritance van de juiste subplaintext in de subs
    ## Gijs: Merci!
    
    def __init__(self, colorNameList):
        """
        from colorama import (                  ## Om de tekst kleur te geven
            Fore,                               ## 
            Style,                              ## 
            init as colorama_init)              ## 
        """
        try:        
            colorNameList = map(lambda x:x.upper(), colorNameList)
            self.init_colors(colorNameList)
        except Exception, e:
            logger.error("something went wrong when initializing colors; " + \
            "did you provide a correct colorNameList %s?", colorNameList)
            logger.error("exception is: %s" % e)
            exit(1)
        colorama_init()
        cursor.hide()
    
    ## any communicator wanting to customize the colors can override
    ## this method to define new colors and styles
    ## TODO: Jo: evt custom perentage style
    ##
    ## Gijs: Wat bedoel je? Bvb de balk verbergen, etc?
    
    def init_colors(self, colorNameList):
        logger.debug("the given colornamelist is %s", colorNameList)
        style = getattr(Style, colorNameList.pop())
        err_color = getattr(Fore, colorNameList.pop())
        wait_color = getattr(Fore, colorNameList.pop())        
        ok_color = getattr(Fore, colorNameList.pop())
        self.ERR_COLOR = err_color #Fore.RED
        self.ERR_STYLE = style #Style.BRIGHT
        self.WAIT_STYLE = style #Style.BRIGHT
        self.WAIT_COLOR = wait_color #Fore.YELLOW
        self.SUCCESS_STYLE = style #Style.BRIGHT
        self.SUCCESS_COLOR = ok_color #Fore.GREEN
        self.FAIL_STYLE = style #Style.BRIGHT
        self.FAIL_COLOR = err_color #Fore.RED
        self.PERC_STYLE = style #Style.BRIGHT
        self.CRITICAL_PERC_COLOR = err_color #Fore.RED
        self.LOW_PERC_COLOR = wait_color #Fore.YELLOW
        self.OK_PERC_COLOR = ok_color #Fore.GREEN

    ## Overrides the printing of an error string on stderr
    def printerr(self, msg):
        sys.stderr.write(self.ERR_STYLE + self.ERR_COLOR + \
        msg + Style.RESET_ALL),
        sys.stderr.flush()

    ## Overrides the printing of a "wait" event on stdout
    def print_wait(self, msg):
        print msg + self.WAIT_STYLE + "[" + self.WAIT_COLOR + \
        "WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        sys.stdout.flush()

    ## Overrides the printing of a "succes" string on stdout
    def print_success(self):
        print self.SUCCESS_STYLE + "[" + self.SUCCESS_COLOR + " OK " + \
        Fore.RESET + "]" + Style.RESET_ALL

    ## Overrides the printing of a "done" string on stdout
    def print_done(self):
        print self.SUCCESS_STYLE + "[" + self.SUCCESS_COLOR + "DONE" + \
        Fore.RESET + "]" + Style.RESET_ALL

    ## Overrides the printing of a "fail" string on stdout
    def print_fail(self):
        print self.FAIL_STYLE + "[" + self.FAIL_COLOR + "FAIL" + \
        Fore.RESET + "]" + Style.RESET_ALL

    ## Overrides the printing of a "balk" string on stdout
    def print_balk(self, percentage):
        if percentage <= 10:
            voorwaardelijke_kleur = self.CRITICAL_PERC_COLOR
        elif 10 < percentage < 60:
            voorwaardelijke_kleur = self.LOW_PERC_COLOR
        else:
            voorwaardelijke_kleur = self.OK_PERC_COLOR
        
        self.print_generic_balk(percentage, self.PERC_STYLE,
        voorwaardelijke_kleur, Fore.RESET, Style.RESET_ALL)

class LoginColoramaCommunicator(SuperColoramaCommunicator, LoginPlaintextCommunicator):
    ## TODO: jo: (hackhackhack) manually override the mutliple inheritance
    ## priorities to avoid quiet printing
    def eventNetloginStart(self):
        LoginPlaintextCommunicator.eventNetloginStart(self)

    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        LoginPlaintextCommunicator.eventLoginGeslaagd(self, downloadpercentage, uploadpercentage)

    def beeindig_sessie(self, error_code=0):
        LoginPlaintextCommunicator.beeindig_sessie(self, error_code)

class LogoutColoramaCommunicator(SuperColoramaCommunicator, LogoutPlaintextCommunicator):
    ## TODO: jo: (hackhackhack) manually override the mutliple inheritance
    ## priorities to avoid quiet printing
    def eventNetloginStart(self):
        LogoutPlaintextCommunicator.eventNetloginStart(self)

    def eventLogoutGeslaagd(self, downloadpercentage, uploadpercentage):
        LogoutPlaintextCommunicator.eventLoginGeslaagd(self, downloadpercentage, uploadpercentage)

    def beeindig_sessie(self, error_code=0):
        LogoutPlaintextCommunicator.beeindig_sessie(self, error_code=0)
