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

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import urllib                           ## Diverse URL-manipulaties
import urlparse                         ## Diverse URL-manipulaties
import socket                           ## Voor ophalen IP
import sys                              ## Basislib
import os                               ## Basislib

import browser

from bs4 import BeautifulSoup, Comment  ## Om webinhoud proper te parsen.

EXIT_FAILURE = 1

class SuperWorker():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        self.co = co
        self.browser = browser.KotnetBrowser(gebruikersnaam, wachtwoord)

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

## A worker class that either succesfull logs you in to kotnet
##  or exits with failure, reporting events to the given communicator
class Kotnetlogin(SuperWorker):
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            self.browser.open_netlogin()
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            sys.exit(EXIT_FAILURE)

    def kuleuven(self):
        self.co.eventKuleuvenStart()
        try:
            self.browser.kies_kuleuven()
            self.co.eventKuleuvenSuccess()
        except:
            self.co.eventKuleuvenFailure()
            sys.exit(EXIT_FAILURE)

    def tegoeden(self):
        tup = self.browser.parse_percentages()

        ## check whether it worked out
        if (len(tup) == 1):
            print tup[0]
        else:
            self.co.eventTegoedenBekend(tup[0], tup[1])

        self.co.beeindig_sessie()

class Dummylogin(Kotnetlogin):
    def __init__(self, co, gebruikersnaam, wachtwoord):
        self.co = co
        self.browser = browser.DummyBrowser(gebruikersnaam, wachtwoord);

## A worker class that either succesfull logs you off from kotnet
##  or exits with failure, reporting events to the given communicator
class Kotnetloguit(SuperWorker):
    def __init__(self, co, gebruikersnaam, wachtwoord, uitteloggenip=None):
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        self.browser = browser.KotnetBrowser(gebruikersnaam, wachtwoord)
        self.co = co

        self.uitteloggenip = uitteloggenip
        if self.uitteloggenip == None:
            ## Lokale IP ophalen: lelijk, maar werkt.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            self.uitteloggenip = s.getsockname()[0]
            s.close()

        ## Formulier aanmaken. Het opsturen van dit formulier geeft toegang
        ## tot de noodzakelijke loguitpagina.
        bestand = open("formulier.html", "w")
        bestand.write("<html><body>\n")
        bestand.write('<FORM METHOD=POST ACTION=' \
        '"https://netlogin.kuleuven.be/cgi-bin/wayf2.pl">\n')
        bestand.write('<INPUT type=hidden name="inout" value="logout">\n')
        bestand.write('<INPUT type=hidden name="ip" value="%s">\n' \
        % self.uitteloggenip)
        bestand.write('<INPUT type=hidden name="network" value="KotNet">\n')
        bestand.write('<INPUT type=hidden name="uid" value="kuleuven/%s">\n' % \
        self.gebruikersnaam)
        bestand.write('<INPUT type=hidden name="lang" value="ned">\n')
        #bestand.write('<INPUT type=submit value="logout">\n')
        bestand.write('<INPUT type=submit value="logout kuleuven/%s@%s">\n' % (self.gebruikersnaam, self.uitteloggenip))
        bestand.write('</FORM>\n')
        bestand.write('</body></html>\n')
        bestand.close()

        self.lokatie_formulier = urlparse.urljoin("file:", \
        urllib.pathname2url(os.path.join(os.getcwd(), "formulier.html")))

    # this is actually the logout
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            self.browser.netlogout(self.lokatie_formulier)
            os.remove(os.path.join(os.getcwd(), "formulier.html"))
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            sys.exit(EXIT_FAILURE)

    def tegoeden(self):
        if (self.browser.parse_logout()):
            print "success!"
        else:
            print "outch!"
        self.co.beeindig_sessie()

class Dummylogout(Kotnetloguit):
    def __init__(self, co, gebruikersnaam, wachtwoord):
        Kotnetloguit.__init__(self, co, gebruikersnaam, wachtwoord)
        self.browser = browser.DummyBrowser(gebruikersnaam, wachtwoord);
