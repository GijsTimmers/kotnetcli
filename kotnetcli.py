#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import curses                           ## Voor mooie output
import argparse                         ## Parst argumenten
import platform                         ## Om te kunnen compileren op Windows
import sys                              ## Basislib
import os                               ## Basislib

import communicator                     ## Voor output op maat
from credentials import Credentials     ## Opvragen van nummer en wachtwoord
from worker import Kotnetlogin          ## Eigenlijke loginmodule

        
def main(co, gebruikersnaam, wachtwoord):
    kl = Kotnetlogin(co, gebruikersnaam, wachtwoord)
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

    parser.add_argument("-q", "--quiet",\
    help="Hides all output",\
    action="store_true")
    
    parser.add_argument("-t", "--plaintext",\
    help="Omits the curses inteface by using plaintext output",\
    action="store_true")

    parser.add_argument("-g", "--guest-mode",\
    help="Logs you in as a different user without forgetting your \
    default credentials",\
    action="store_true")


    argumenten = parser.parse_args()
    return argumenten

def aanstuurderObvArgumenten(argumenten, cr):
    argumententuple_omgekeerd = [not i for i in vars(argumenten).values()]
    if argumenten.forget:
        print "ik wil vergeten"
        cr.forget()
        return()
    
    if argumenten.guest_mode:
        ## werkt alleen met login op het moment
        print "ik wil me anders voordoen dan ik ben"
        gebruikersnaam, wachtwoord = cr.guest()
        co = communicator.CursesCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        #curses.wrapper(main, gebruikersnaam, wachtwoord)
        
    if argumenten.quiet:
        print "ik wil zwijgen"
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.QuietCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        ## needs to be removed, but if I do that, it will log in as normal
        ## login mode
    
    if argumenten.plaintext:
        print "ik wil terug naar de basis"
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.PlaintextCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        ## needs to be removed, but if I do that, it will log in as normal
        ## login mode
        
    if argumenten.logout:
        print "ik wil uitloggen"
        print "(Nog niet geïmplementeerd)"
        return()
    
    if argumenten.login:    
        print "ik wil inloggen"
        gebruikersnaam, wachtwoord = cr.getset()
        if os.name == "posix":
            co = communicator.CursesCommunicator()
            main(co, gebruikersnaam, wachtwoord)
        else:
            co = communicator.PlaintextCommunicator()
            main(co, gebruikersnaam, wachtwoord)
    
    print "ik wil inloggen"
    gebruikersnaam, wachtwoord = cr.getset()
    if os.name == "posix":
        co = communicator.CursesCommunicator()
        main(co, gebruikersnaam, wachtwoord)
    else:
        co = communicator.PlaintextCommunicator()
        main(co, gebruikersnaam, wachtwoord)
    
cr = Credentials()
aanstuurderObvArgumenten(argumentenParser(), cr)
