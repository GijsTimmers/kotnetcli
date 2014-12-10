#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To  view a copy of 
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

version = "1.3.0-dev"

def main(co, gebruikersnaam, wachtwoord, actie="inloggen"):
    if actie == "inloggen":
        #ping(co)
        kl = worker.Kotnetlogin(co, gebruikersnaam, wachtwoord)
    elif actie == "uitloggen":
        #ping(co)
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

def mainLoginprocedure(co, gebruikersnaam, wachtwoord, dummy=False):
    kl = worker.Kotnetlogin(co, gebruikersnaam, wachtwoord)
    if dummy == True:
        kl = worker.Dummylogin(co, gebruikersnaam, wachtwoord)
        ## kl remains Kotnetlogin if dummy mode is not activated.
            
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()
    
def mainLoguitprocedure(co, gebruikersnaam, wachtwoord, dummy=False):
    kl = worker.Kotnetloguit(co, gebruikersnaam, wachtwoord)
    if dummy == True:
        kl = worker.Dummyloguit(co, gebruikersnaam, wachtwoord)
            
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()

def mainForceerLoginprocedure(co, gebruikersnaam, wachtwoord, dummy=False):
    kl = worker.Kotnetlogin(co, gebruikersnaam, wachtwoord, afsluiten=False)
    
    ## IP van uit te loggen apparaat opzoeken
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()
    uitteloggenip = kl.uitteloggenipophalen()
    print uitteloggenip
    
    ## Ander apparaat uitloggen
    kl = worker.Kotnetloguit(co, gebruikersnaam, wachtwoord, uitteloggenip=uitteloggenip)
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()
    
    ## Conventionele login
    kl = worker.Kotnetlogin(co, gebruikersnaam, wachtwoord)
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()

def argumentenParser():
    parser = argparse.ArgumentParser(description="Script om in- of uit \
    te loggen op KotNet")
    
    workergroep = parser.add_mutually_exclusive_group()
    credentialsgroep = parser.add_mutually_exclusive_group()
    communicatorgroep = parser.add_mutually_exclusive_group()
    
    ## We create three different groups, whose arguments can't be mixed (using
    ## the add_mutually_exclusive_group() option. If you enter non-combinable
    ## options, you'll get an error.
    
    ## Then, we create three dests: worker, credentials and communicator. 
    ## The value to each of these dests depends on the flags the user applies.
    ## If he applies none, each dest will use a default value, set with the
    ## default parameter in add_argument().
    
    ## These two things void the need for complex decision trees.
    
    workergroep.add_argument("-i", "--login",\
    help="Logs you in on KotNet (default)",\
    action="store_const", dest="worker", const="login", default="login")
    
    workergroep.add_argument("-!", "--force-login",\
    help="Logs you out on other IP's, and then in on this one",\
    action="store_const", dest="worker", const="force_login")

    workergroep.add_argument("-o", "--logout",\
    help="Logs you out off KotNet",\
    action="store_const", dest="worker", const="logout")
    
    workergroep.add_argument("-1", "--dummy-login",\
    help="Performs a dry-run logging in",\
    action="store_const", dest="worker", const="dummy_login")
    
    workergroep.add_argument("-0", "--dummy-logout",\
    help="Performs a dry-run logging out",\
    action="store_const", dest="worker", const="dummy_logout")
    
    credentialsgroep.add_argument("-k", "--keyring",\
    help="Makes kotnetcli pick up your credentials from the keyring (default)",\
    action="store_const", dest="credentials", const="keyring", \
    default="keyring")

    credentialsgroep.add_argument("-f", "--forget",\
    help="Makes kotnetcli forget your credentials",\
    action="store_const", dest="credentials", const="forget")
    
    credentialsgroep.add_argument("-g", "--guest-mode",\
    help="Logs you in as a different user without forgetting your \
    default credentials",\
    action="store_const", dest="credentials", const="guest_mode")
    
    communicatorgroep.add_argument("-c", "--color",\
    help="Logs you in using colored text output (default)",\
    action="store_const", dest="communicator", const="colortext", \
    default="colortext")
    
    """
    communicatorgroep.add_argument("-a", "--android",\
    help="Logs you in using the Android login system",\
    action="store_const", dest="communicator", const="android")
    """
    
    communicatorgroep.add_argument("-u", "--curses",\
    help="Logs you in using curses output",\
    action="store_const", dest="communicator", const="curses")
    
    communicatorgroep.add_argument("-t", "--plaintext",\
    help="Omits the curses interface by using plaintext output",\
    action="store_const", dest="communicator", const="plaintext")
    
    communicatorgroep.add_argument("-d", "--dialog",\
    help="Omits the curses interface by using dialog based output",\
    action="store_const", dest="communicator", const="dialog")
    
    communicatorgroep.add_argument("-b", "--bubble",\
    help="Hides all output except for a bubble notification",\
    action="store_const", dest="communicator", const="bubble")
    
    communicatorgroep.add_argument("-s", "--summary",\
    help="Hides all output except for a short summary",\
    action="store_const", dest="communicator", const="summary")

    communicatorgroep.add_argument("-q", "--quiet",\
    help="Hides all output",\
    action="store_const", dest="communicator", const="quiet")
    
    parser.add_argument("-v", "--version", action="version", version=version)
        
    argumenten = parser.parse_args()
    #print argumenten.__dict__
    
    return(argumenten)
    
def aanstuurderObvArgumenten(argumenten):    
    ############## 1. parse credential-related flags ##############
    cr = Credentials()
    #print argumenten.__dict__
    if argumenten.worker == "dummy_login" or argumenten.worker == "dummy_logout":
        print "ik wil credentials ophalen voor spek en bonen"
        gebruikersnaam, wachtwoord = cr.dummy()

    else:
        if argumenten.credentials == "keyring":
            print "ik haal de credentials uit de keyring"
            gebruikersnaam, wachtwoord = cr.getset()
        
        elif argumenten.credentials == "forget":
            print "ik wil vergeten"
            cr.forget()
            exit(0)
        
        elif argumenten.credentials == "guest_mode":
            print "ik wil me anders voordoen dan ik ben"
            gebruikersnaam, wachtwoord = cr.guest()
    
        
    ############## 2. switch on communicator-related flags ##############
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
        co = communicator.ColoramaCommunicator()
    
    elif argumenten.communicator == "plaintext":
        print "ik wil terug naar de basis"
        co = communicator.PlaintextCommunicator()
    
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
    
    ############## 3. switch on login-type flags ##############    
    if argumenten.worker == "login":
        print "ik wil inloggen"
        mainLoginprocedure(co, gebruikersnaam, wachtwoord)
    
    elif argumenten.worker == "force_login":
        print "ik moet en zal inloggen"
        mainForceerLoginprocedure(co, gebruikersnaam, wachtwoord)
    
    elif argumenten.worker == "logout":
        print "ik wil uitloggen"
        mainLoguitprocedure(co, gebruikersnaam, wachtwoord)
        
    
    
    elif argumenten.worker == "dummy_login":
        print "ik wil inloggen voor spek en bonen"
        mainLoginprocedure(co, gebruikersnaam, wachtwoord, dummy=True)
    
    elif argumenten.worker == "dummy_logout":
        print "ik wil uitloggen voor spek en bonen"
        mainLoguitprocedure(co, gebruikersnaam, wachtwoord, dummy=True)

aanstuurderObvArgumenten(argumentenParser())
