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

import socket
import urlparse
import urllib
import mechanize                        ## Emuleert een browser
import time                             ## Voor timeout om venster te sluiten
import re                               ## Basislib voor reguliere expressies
import sys ## tijdelijk, haal later weg
import os ## tijdelijk, haal later weg

class Kotnetlogin():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            respons = self.browser.open("https://netlogin.kuleuven.be", \
            timeout=1.8)
            html = respons.read()
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            sys.exit(1)
        
    def kuleuven(self):
        self.co.eventKuleuvenStart()
        try:
            self.browser.select_form(nr=1)
            self.browser.submit()
            self.co.eventKuleuvenSuccess()
        except:
            self.co.eventKuleuvenFailure()
            sys.exit(1)

    def gegevensinvoeren(self):
        self.co.eventInvoerenStart()
        try:
            self.browser.select_form(nr=1)
            self.browser.form["uid"] = self.gebruikersnaam
            wachtwoordvaknaam = \
            self.browser.form.find_control(type="password").name
            
            self.browser.form[wachtwoordvaknaam] = self.wachtwoord
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            sys.exit(1)
        
        
    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            self.browser.submit()
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            sys.exit(1)
        
        
    def tegoeden(self):
        html = self.browser.response().read()
        #print html
        zoekresultaten = (re.findall("<br>\(\d*%\)</TD>", html))
        #print zoekresultaten
        ## zoek naar: <br>(40%)</TD>
        self.downloadpercentage = int(zoekresultaten[0]\
        .strip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%()<>br/"))
        self.uploadpercentage   = int(zoekresultaten[1]\
        .strip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%()<>br/"))
        
        self.co.eventTegoedenBekend(self.downloadpercentage, \
        self.uploadpercentage)
        #self.co.eventDownloadtegoedBekend(self.downloadpercentage)
        #self.co.eventUploadtegoedBekend(self.uploadpercentage)

        self.co.beeindig_sessie()

class Kotnetloguit():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        
        ## Lokale IP ophalen: lelijk, maar werkt.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.lokaleip = s.getsockname()[0]
        s.close()
        
        ## Formulier aanmaken. Het opsturen van dit formulier geeft toegang
        ## tot de noodzakelijke loguitpagina. 
        bestand = open("formulier.html", "w")
        bestand.write("<html><body>\n")
        bestand.write('<FORM METHOD=POST ACTION=' \
        '"https://netlogin.kuleuven.be/cgi-bin/wayf2.pl">\n')
        bestand.write('<INPUT type=hidden name="inout" value="logout">\n')
        bestand.write('<INPUT type=hidden name="ip" value="%s">\n' \
        % self.lokaleip)
        bestand.write('<INPUT type=hidden name="network" value="KotNet">\n')
        bestand.write('<INPUT type=hidden name="uid" value="kuleuven/%s">\n' % \
        self.gebruikersnaam)
        bestand.write('<INPUT type=hidden name="lang" value="ned">\n')
        bestand.write('<INPUT type=submit value="logout">\n')
        bestand.write('</FORM>\n')
        bestand.write('</body></html>\n')
        bestand.close()
        
        self.lokatie_formulier = urlparse.urljoin("file:", \
        urllib.pathname2url(os.path.join(os.getcwd(), "formulier.html")))
    
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            self.browser.open(self.lokatie_formulier, timeout=1.8)                        
            self.browser.select_form(nr=0)
            self.browser.submit()
            os.remove(os.path.join(os.getcwd(), "formulier.html"))
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            sys.exit(1)
    
    def kuleuven(self):
        pass
    
    def gegevensinvoeren(self):
        self.co.eventInvoerenStart()
        try:
            self.browser.select_form(nr=1)
            wachtwoordvaknaam = \
            self.browser.form.find_control(type="password").name
            self.browser.form[wachtwoordvaknaam] = self.wachtwoord
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            sys.exit(1)
    
    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            self.browser.submit()
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            sys.exit(1)
    
    def tegoeden(self):
        self.co.beeindig_sessie()
    
        
class Dummylogin():
    pass
