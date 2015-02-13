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

## kotnetcli.py: encapsulates the end-user command line interface. It parses
## the command line arguments to:
##  - create the appropriate credentials instance
##  - create the appropriate communicator instance
##  - create and start the appropriate worker instance

#jo: zijn alle imports hieronder nog nodig?
import subprocess                       ## Om systeemcommando's uit te voeren
import argparse                         ## Parst argumenten
import platform                         ## Om te kunnen compileren op Windows
import sys                              ## Basislib
import os                               ## Basislib

from communicator.fabriek import LoginCommunicatorFabriek, LogoutCommunicatorFabriek    ## Voor output op maat

## Gijs: In de toekomst graag vervangen door fabriek

from credentials import Credentials     ## Opvragen van nummer en wachtwoord
from worker import LoginWorker, LogoutWorker #, ForceerLoginWorker

version = "1.3.0-dev"

## An argument parse action that prints license information
## on stdout and exits
class PrintLicenceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print "This work is licensed under the Creative Commons"
        print "Attribution-ShareAlike 4.0 International License. To  view a copy of"
        print "this license, visit https://creativecommons.org/licenses/by-sa/4.0/ or"
        print "send a letter to Creative Commons, PO Box 1866, Mountain View,"
        print "CA 94042, USA.\n"
        print "Visit the github page (https://github.com/GijsTimmers/kotnetcli) to"
        print "view the full source code and to collaborate on the project."
        exit(0)

## A class encapsulating the argument parsing behavior
## Note: directly inherit from "object" in order to be able to use super() in child classes
class KotnetCLI(object):
    
    ## Note: create the parser and groups as instance fiels so subclasses can access them
    ##
    ## We create three different groups, whose arguments can't be mixed (using
    ## the add_mutually_exclusive_group() option. If you enter non-combinable
    ## options, you'll get an error.
    ## Then, we create three dests: worker, credentials and communicator.
    ## The value to each of these dests depends on the flags the user applies.
    ## If he applies none, each dest will use a default value, set with the
    ## default parameter in add_argument().
    ## These two things void the need for complex decision trees.
    def __init__(self, descr="Script om in- of uit te loggen op KotNet"):
        self.parser = argparse.ArgumentParser(descr)
        self.workergroep = self.parser.add_mutually_exclusive_group()
        self.credentialsgroep = self.parser.add_mutually_exclusive_group()
        self.communicatorgroep = self.parser.add_mutually_exclusive_group()
        self.voegArgumentenToe()
    
    def voegArgumentenToe(self):
        ## general flags
        self.parser.add_argument("-v", "--version", action="version", version=version)
        self.parser.add_argument("-l", "--license", action=PrintLicenceAction, nargs=0)
        
        ## login type flags
        self.workergroep.add_argument("-i", "--login",\
        help="Logs you in on KotNet (default)",\
        action="store_const", dest="worker", const="login", default="login")

        self.workergroep.add_argument("-o", "--logout",\
        help="Logs you out off KotNet",\
        action="store_const", dest="worker", const="logout")
        
        '''
        self.workergroep.add_argument("-!", "--force-login",\
        help="Logs you out on other IP's, and then in on this one",\
        action="store_const", dest="worker", const="force_login")
        '''
        
        ## credentials type flags
        self.credentialsgroep.add_argument("-k", "--keyring",\
        help="Makes kotnetcli pick up your credentials from the keyring (default)",\
        action="store_const", dest="credentials", const="keyring", \
        default="keyring")
        
        self.credentialsgroep.add_argument("-f", "--forget",\
        help="Makes kotnetcli forget your credentials",\
        action="store_const", dest="credentials", const="forget")
        
        self.credentialsgroep.add_argument("-g", "--guest-mode",\
        help="Logs you in as a different user without forgetting your \
        default credentials",\
        action="store_const", dest="credentials", const="guest_mode")
        
        ## communicator flags
        self.communicatorgroep.add_argument("-t", "--plaintext",\
        help="Omits the curses interface by using plaintext output",\
        action="store_const", dest="communicator", const="plaintext")
        
        self.communicatorgroep.add_argument("-c", "--color",\
        help="Logs you in using colored text output (default)",\
        action="store_const", dest="communicator", const="colortext", \
        default="colortext")
        
        ## voorlopig andere communicators uitschakelen in de dev branch
        '''
        """
        communicatorgroep.add_argument("-a", "--android",\
        help="Logs you in using the Android login system",\
        action="store_const", dest="communicator", const="android")
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
        '''
    
    ## Parses the arguments corresponding to self.parser
    def parseArgumenten(self):
        argumenten = self.parser.parse_args()
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
        '''cr = Credentials()
        if argumenten.credentials == "keyring":
            print "ik haal de credentials uit de keyring"
            gebruikersnaam, wachtwoord = cr.getset()
        
        elif argumenten.credentials == "forget":
            print "ik wil vergeten"
            cr.forget()
            exit(0)
       
        elif argumenten.credentials == "guest_mode":
            print "ik wil me anders voordoen dan ik ben"
            gebruikersnaam, wachtwoord = cr.guest()'''

    ## returns tuple (worker, fabriek)
    def parseActionFlags(self, argumenten):
        if argumenten.worker == "login":
            print "ik wil inloggen"
            worker = LoginWorker()
            fabriek = LoginCommunicatorFabriek()
        
        elif argumenten.worker == "logout":
            print "ik wil uitloggen"
            worker = LogoutWorker()
            fabriek = LogoutCommunicatorFabriek()
        
        '''elif argumenten.worker == "force_login":
            print "ik moet en zal inloggen"
            worker = ForceLoginWorker()
            fabriek = LoginCommunicatorFabriek()
        '''
        
        return (worker, fabriek)
    
    ## returns communicator
    def parseCommunicatorFlags(self, fabriek, argumenten):
        if argumenten.communicator == "plaintext":
            print "ik wil terug naar de basis"
            return fabriek.createPlaintextCommunicator()
        
        elif argumenten.communicator == "colortext":
            print "ik wil vrolijke kleuren"
            return fabriek.createColoramaCommunicator()
        
        else:
            print "ik ga mee met de stroom" # TODO kunnen we default niet specifieren mbv argparse module??
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


## Start de zaak asa deze file rechtstreeks aangeroepen is vanuit
## command line (i.e. niet is geimporteerd vanuit een andere file)
if  __name__ =='__main__':
    print "== kotnetcli started =="
    k = KotnetCLI()
    k.parseArgumenten()
    print "== kotnetcli done =="
