#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import subprocess                       ## Om systeemcommando's uit te voeren
import argparse                         ## Parst argumenten
import platform                         ## Om te kunnen compileren op Windows
import sys                              ## Basislib
import os                               ## Basislib

import communicator                     ## Voor output op maat
from credentials import Credentials     ## Opvragen van nummer en wachtwoord
import worker                           ## Eigenlijke loginmodule
from pinger import ping                 ## Checken of we op KUL-net zitten


def main(co, gebruikersnaam, wachtwoord, actie="inloggen"):
    if actie == "inloggen":
        ping(co)
        kl = worker.Kotnetlogin(co, gebruikersnaam, wachtwoord)
    elif actie == "uitloggen":
        ping(co)
        kl = worker.Kotnetloguit(co, gebruikersnaam, wachtwoord)
    elif actie == "dummyinloggen":
        kl = worker.Dummylogin(co, gebruikersnaam, wachtwoord)
    elif actie == "dummyuitloggen":
        kl = worker.Dummyloguit(co, gebruikersnaam, wachtwoord)
            
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()

def argumentenParser():
    parser = argparse.ArgumentParser(description="Script om in- of uit \
    te loggen op KotNet")

    parser.add_argument("-i", "--login",\
    help="Logs you in on KotNet (default)",\
    action="store_true")

    parser.add_argument("-o", "--logout",\
    help="Logs you out off KotNet",\
    action="store_true")

    parser.add_argument("-f", "--forget",\
    help="Makes kotnetcli forget your credentials",\
    action="store_true")
    
    parser.add_argument("-g", "--guest-mode",\
    help="Logs you in as a different user without forgetting your \
    default credentials",\
    action="store_true")
    
    parser.add_argument("-c", "--colortext",\
    help="Omits the curses interface by using colortext output",\
    action="store_true")
    
    parser.add_argument("-t", "--plaintext",\
    help="Omits the curses interface by using plaintext output",\
    action="store_true")
    
    parser.add_argument("-d", "--dialog",\
    help="Omits the curses inteface by using dialog based output",\
    action="store_true")
    
    parser.add_argument("-b", "--bubble",\
    help="Hides all output except for a bubble notification",\
    action="store_true")
    
    parser.add_argument("-s", "--summary",\
    help="Hides all output except for a small summary",\
    action="store_true")

    parser.add_argument("-q", "--quiet",\
    help="Hides all output",\
    action="store_true")
    
    parser.add_argument("-1", "--dummy-login",\
    help="Performs a dry-run logging in",\
    action="store_true")
    
    parser.add_argument("-2", "--dummy-logout",\
    help="Performs a dry-run logging out",\
    action="store_true")

    argumenten = parser.parse_args()
    return argumenten

def aanstuurderObvArgumenten(argumenten):
    
    ############## 1. parse credential-related flags ##############
    cr = Credentials()
    if argumenten.forget:
        print "ik wil vergeten"
        cr.forget()
        return()
    
    if argumenten.guest_mode:
        print "ik wil me anders voordoen dan ik ben"
        gebruikersnaam, wachtwoord = cr.guest()
    else:
        print "ik haal de credentials uit de keyring"
        gebruikersnaam, wachtwoord = cr.getset()
        
    ############## 2. switch on communicator-related flags ##############
        
    if argumenten.colortext:
        print "ik wil wat kleur in mijn leven aanbrengen"
        co = communicator.ColoramaCommunicator()
        
    elif argumenten.plaintext:
        print "ik wil terug naar de basis"
        co = communicator.PlaintextCommunicator()
    
    elif argumenten.dialog:
        print "ik wil fancy dialogs"
        co = communicator.DialogCommunicator()
    
    elif argumenten.bubble:
        print "ik wil bellen blazen"
        co = communicator.BubbleCommunicator()
    
    elif argumenten.summary:
        print "ik wil het mooie in de kleine dingen zien"
        co = communicator.SummaryCommunicator()
        
    elif argumenten.quiet:
        print "ik wil zwijgen"
        co = communicator.QuietCommunicator()
    else:
        ## no communicator specified; choose default communicator
        print "standaard communicator gekozen"
        if os.name == "posix":
            co = communicator.CursesCommunicator()
        else:
            co = communicator.ColoramaCommunicator()
    
    ############## 3. switch on login-type flags ##############
    
    if argumenten.dummy_login:
        print "ik wil inloggen voor spek en bonen"
        main(co, gebruikersnaam, wachtwoord, actie="dummyinloggen")
    
    elif argumenten.dummy_logout:
        print "ik wil uitloggen voor spek en bonen"
        main(co, gebruikersnaam, wachtwoord, actie="dummyuitloggen")
    
    elif argumenten.logout:
        print "ik wil uitloggen"
        main(co, gebruikersnaam, wachtwoord, actie="uitloggen")
    
    elif argumenten.login:    
        print "ik wil inloggen met een --login vlag"
        main(co, gebruikersnaam, wachtwoord, actie="inloggen")
    
    else:
        print "ik wil inloggen zonder vlag"
        main(co, gebruikersnaam, wachtwoord, actie="inloggen")


aanstuurderObvArgumenten(argumentenParser())

"""
if ping() == True:
    aanstuurderObvArgumenten(argumentenParser())
    sys.exit(0)
else:
    print "Niet verbonden met het KU Leuven-netwerk."
    sys.exit(1)
"""
