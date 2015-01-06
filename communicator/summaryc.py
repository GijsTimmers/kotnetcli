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

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import sys                              ## Basislib
import os                               ## Basislib
import platform                         ## Om onderscheid Lin/Mac te maken
from quietc import QuietCommunicator
from tools import cursor                ## Om cursor te verbergen/tonen
#from ..tools import cursor              ## Om cursor te verbergen/tonen

## Gijs:
## We hoeven geen relatieve import te gebruiken omdat de map waarin 
## kotnetcli.py zich bevindt de rootmap ($PYTHONPATH) is. De map 'tools'
## bevindt zich daar ook; daarom hoeven we niet te verwijzen naar de lokatie
## ten opzichte van deze specifieke communicator (denk ik)

if os.name == "nt":
    try:            
        from colorama import (              ## Voor gekleurde tekst.
            Fore,
            Style,
            init
            )
    except ImportError:
        print "Couldn't import the colorama library."
        pass


if os.name == "posix" and platform.system() == "Darwin": ## Is een Mac
    try:            
        from colorama import (              ## Voor gekleurde tekst.
            Fore,
            Style,
            init
            )
    except ImportError:
        print "Couldn't import the colorama library."
        pass


if os.name == "posix" and platform.system() != "Darwin": ## Is een Linux
    print "Import Linux stuff"

    try:            
        import curses                       ## Voor tekenen op scherm.
    except ImportError:
        print "Couldn't import the curses library."
        pass
    try:            
        import notify2                      ## OS-specifieke notificaties
    except ImportError:
        print "Couldn't import the notify2 library."
        pass
    try:            
        from dialog import Dialog           ## Voor tekenen op scherm.
    except ImportError:
        print "Couldn't import the dialog library."
        pass
    
    try:            
        from colorama import (              ## Voor gekleurde tekst.
            Fore,
            Style,
            init
            )
    except ImportError:
        print "Couldn't import the colorama library."
        pass
        
## Abstract super class (not intended to directly create), encapsulating 
## things common to a Login- and LogoutSummaryCommunicator
class SuperSummaryCommunicator(QuietCommunicator):
    def eventPingFailure(self):
        print "Niet verbonden met het KU Leuven-netwerk."
    def eventPingAlreadyOnline(self):
        print "U bent al online."

class LoginSummaryCommunicator(SuperSummaryCommunicator):
    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        print "Login geslaagd."
        print "Download: " + str(downloadpercentage) + "%" + ",",
        print "Upload: " + str(uploadpercentage) + "%"

    def beeindig_sessie(self, error_code=0):
        if error_code == 0:
            pass
        else:
            print "Login mislukt."

class LogoutSummaryCommunicator(SuperSummaryCommunicator):
    def eventLogoutGeslaagd(self):
        print "Logout geslaagd."
        
    def beeindig_sessie(self, error_code=0):
        if error_code == 0:
            pass
        else:
            print "Logout mislukt."

