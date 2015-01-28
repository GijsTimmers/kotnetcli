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

## worker.py: zorgt voor het goed verlopen van de login of logout:
## - stuurt een credentials-ophaalcommando door naar het credentialsobject cr,
##   zonder te weten wat voor een type credentialsklasse dat precies is;
## - stuurt de statusberichten door naar de communicator co, zonder te weten
##   wat er precies wordt afgebeeld, en hoe;
## - stuurt de login- en logoutcommando's door naar het browserobject br.


import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import urllib                           ## Diverse URL-manipulaties
import browser                          ## Doet het eigenlijke browserwerk
import urlparse                         ## Diverse URL-manipulaties
import mechanize                        ## Emuleert een browser
import socket                           ## Voor ophalen IP
import sys                              ## Basislib
import os                               ## Basislib

from tools import pinger                ## Om te checken of we op Kotnet zitten
from tools import errorcodes as error   ## Om magic number errors te voorkomen
from bs4 import BeautifulSoup, Comment  ## Om webinhoud proper te parsen.

EXIT_FAILURE = 1 ## Tijdelijke exitcode, moet nog worden geïmplementeerd.

class SuperWorker():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        self.co = co
        self.browser = browser.KotnetBrowser(gebruikersnaam, wachtwoord)
    
    """ Reden voor uitcommenten: Browser() gebruikt geen abstracte klasses. 
    Daardoor is login_input_credentials() heel anders dan logout_input_creden-
    tials en kunnen we niet input_credentials() aanroepen.
    
    def go(self):
        self.netlogin()
        self.kuleuven()
        self.gegevensinvoeren()
        self.gegevensopsturen()
        self.tegoeden()

    def netlogin(self):
            pass

    def kuleuven(self):
            pass

    def gegevensinvoeren(self):
        self.co.eventInvoerenStart()
        try:
            self.browser.input_credentials()
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            sys.exit(EXIT_FAILURE)

    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            self.browser.send_credentials()
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            sys.exit(EXIT_FAILURE)

    def tegoeden(self):
            pass
    """

## A worker class that either succesfull logs you in to kotnet
## or exits with failure, reporting events to the given communicator
class Kotnetlogin(SuperWorker):
    def go(self):
        self.netlogin()
        self.kuleuven()
        self.gegevensinvoeren()
        self.gegevensopsturen()
        self.resultaten()
        
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            self.browser.login_open_netlogin()
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            sys.exit(EXIT_FAILURE)

    def kuleuven(self):
        self.co.eventKuleuvenStart()
        try:
            self.browser.login_kies_kuleuven()
            self.co.eventKuleuvenSuccess()
        except:
            self.co.eventKuleuvenFailure()
            sys.exit(EXIT_FAILURE)
    
    def gegevensinvoeren(self):
        self.co.eventInvoerenStart()
        try:
            self.browser.login_input_credentials()
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            sys.exit(EXIT_FAILURE)

    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            self.browser.login_send_credentials()
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            sys.exit(EXIT_FAILURE)

    def resultaten(self):
        tup = self.browser.login_parse_results()
        ## check whether it worked out
        if len(tup) == 1:
            print tup[0]
        else:
            self.co.eventResultatenBekend(tup[0], tup[1])
        self.co.beeindig_sessie()

class Dummylogin(Kotnetlogin):
    def __init__(self, co, gebruikersnaam, wachtwoord):
        self.co = co
        self.browser = browser.DummyBrowser(gebruikersnaam, wachtwoord);

## A worker class that either succesfull logs you off from kotnet
## or exits with failure, reporting events to the given communicator
## Do not use Kotnetlogout for integration in a forced-login method. We have
## KotnetForceLogin() for this purpose.
class Kotnetlogout(SuperWorker):
    def go(self):
        self.formulieropsturen()
        self.resultaten()
    
    def formulieraanmaken(self):
        self.co.eventFormulierAanmakenStart()
        try:
            self.browser.logout_input_credentials()
            self.co.eventFormulierAanmakenSuccess()
        except:
            self.co.eventFormulierAanmakenFailure()
            sys.exit(EXIT_FAILURE)
    
    def formulieropsturen(self):
        self.co.eventFormulierOpsturenStart()
        try:
            self.browser.logout_send_credentials()
            self.co.eventFormulierOpsturenSuccess()
        except:
            self.co.eventFormulierOpsturenFailure()
            sys.exit(EXIT_FAILURE)

    def resultaten(self):
        if logout_parse_results():
            print "success!"
        else:
            print "outch!"
        self.co.beeindig_sessie()

class Dummylogout(Kotnetlogout):
    def __init__(self, co, gebruikersnaam, wachtwoord):
        Kotnetlogout.__init__(self, co, gebruikersnaam, wachtwoord)
        self.browser = browser.DummyBrowser(gebruikersnaam, wachtwoord);

class KotnetForceer(Kotnetlogin):
    def __init__(self, co, gebruikersnaam, wachtwoord):
        self.my_super_kl = Kotnetlogin.__init__(self, co, gebruikersnaam, wachtwoord)

    def go(self):
        ## IP van uit te loggen apparaat opzoeken
        self.netlogin()
        self.kuleuven()
        self.gegevensinvoeren()
        self.gegevensopsturen()
        self.oudipophalen() ## te implementeren
        ## Uitloggen
        self.formulieropsturen()
        self.logoutresultaten() ## te implementeren
        self.netlogin()
        self.kuleuven()
        self.gegevensinvoeren()
        self.gegevensopsturen()
        self.loginresultaten()
    
