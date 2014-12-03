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
    if argumenten.forget:
        print "ik wil vergeten"
        cr = Credentials()
        cr.forget()
        return()
    
    if argumenten.guest_mode:
        ## werkt alleen met login op het moment
        print "ik wil me anders voordoen dan ik ben"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.guest()
        co = communicator.CursesCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        #curses.wrapper(main, gebruikersnaam, wachtwoord)
        
    if argumenten.colortext:
        print "ik wil wat kleur in mijn leven aanbrengen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.ColoramaCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        
    if argumenten.plaintext: ## Gekaapt voor Kotnetloguit()
        print "ik wil terug naar de basis"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.PlaintextCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        ## needs to be removed, but if I do that, it will log in as normal
        ## login mode
    
    if argumenten.dialog:
        print "ik wil fancy dialogs"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.DialogCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
    
    if argumenten.bubble:
        print "ik wil bellen blazen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.BubbleCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
    
    if argumenten.summary:
        print "ik wil het mooie in de kleine dingen zien"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.SummaryCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        
    if argumenten.quiet:
        print "ik wil zwijgen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.QuietCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        ## needs to be removed, but if I do that, it will log in as normal
        ## login mode
    
    if argumenten.dummy_login:
        print "ik wil inloggen voor spek en bonen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.dummy()
        co = communicator.ColoramaCommunicator()
        main(co, gebruikersnaam, wachtwoord, actie="dummyinloggen")
        return()
    
    if argumenten.dummy_logout:
        print "ik wil uitloggen voor spek en bonen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.dummy()
        co = communicator.ColoramaCommunicator()
        main(co, gebruikersnaam, wachtwoord, actie="dummyuitloggen")
        return()
    
    if argumenten.logout:
        print "ik wil uitloggen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.ColoramaCommunicator()
        main(co, gebruikersnaam, wachtwoord, actie="uitloggen")
        return()
    
    if argumenten.login:    
        print "ik wil inloggen"
        cr = Credentials()
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.ColoramaCommunicator()
        main(co, gebruikersnaam, wachtwoord, actie="inloggen")
        return()
    
    print "ik wil inloggen"
    cr = Credentials()
    gebruikersnaam, wachtwoord = cr.getset()
    if os.name == "posix":
        co = communicator.CursesCommunicator()
        main(co, gebruikersnaam, wachtwoord)
    else:
        co = communicator.ColoramaCommunicator()
        main(co, gebruikersnaam, wachtwoord)

aanstuurderObvArgumenten(argumentenParser())

"""
if ping() == True:
    aanstuurderObvArgumenten(argumentenParser())
    sys.exit(0)
else:
    print "Niet verbonden met het KU Leuven-netwerk."
    sys.exit(1)
"""
