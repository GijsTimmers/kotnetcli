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

import mechanize                        ## Emuleert een browser
import time                             ## Voor timeout om venster te sluiten
import re                               ## Basislib voor reguliere expressies

class Kotnetlogin():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        
        self.co.kprint(0, 0, "Netlogin openen.......")
        self.co.kprint(0, 22, "[    ]", self.co.tekstOpmaakVet)
        #self.co.kprint(0, 23, "WAIT", co.tekstOpmaakVet | co.tekstKleurGeel)
        self.co.kprint(0, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
        self.co.kprint(1, 0, "KU Leuven kiezen......")
        self.co.kprint(1, 22, "[    ]", self.co.tekstOpmaakVet)
        self.co.kprint(2, 0, "Gegevens invoeren.....")
        self.co.kprint(2, 22, "[    ]", self.co.tekstOpmaakVet)
        self.co.kprint(3, 0, "Gegevens opsturen.....")
        self.co.kprint(3, 22, "[    ]", self.co.tekstOpmaakVet)
        self.co.kprint(4, 0, "Download:")
        self.co.kprint(4, 10, "[          ][    ]", self.co.tekstOpmaakVet)
        self.co.kprint(5, 0, "Upload:")
        self.co.kprint(5, 10, "[          ][    ]", self.co.tekstOpmaakVet)
    
    def netlogin(self):
        try:
            respons = self.browser.open("https://netlogin.kuleuven.be", \
            timeout=1.8)
            html = respons.read()
            self.co.kprint(0, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            self.co.kprint(1, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
        except:
            self.co.kprint(0, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            print "JA"
            sys.exit(1)
        
    def kuleuven(self):
        try:
            self.browser.select_form(nr=1)
            self.browser.submit()
            self.co.kprint(1, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            self.co.kprint(2, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
        except:
            self.co.kprint(1, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            exit(1)
        

    def gegevensinvoeren(self):
        try:
            self.browser.select_form(nr=1)
            self.browser.form["uid"] = self.gebruikersnaam
            wachtwoordvaknaam = \
            self.browser.form.find_control(type="password").name
            
            self.browser.form[wachtwoordvaknaam] = self.wachtwoord
            self.co.kprint(2, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            self.co.kprint(3, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            self.co.kprint(4, 14, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            self.co.kprint(4, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            self.co.kprint(5, 14, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            self.co.kprint(5, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
        except:
            self.co.kprint(2, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            exit(1)
        
        
    def gegevensopsturen(self):
        try:
            self.browser.submit()
            self.co.kprint(3, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
        except:
            self.co.kprint(3, 23, "FAIL", self.co.tekstKleurGeelOpmaakVet) 
            exit(1)
        
        
    def tegoeden(self):
        ## Tegoeden parsen
        html = self.browser.response().read()
        #print html
        zoekresultaten = (re.findall("<br>\(\d*%\)</TD>", html))
        #print zoekresultaten
        ## zoek naar: <br>(40%)</TD>
        self.downloadpercentage = int(zoekresultaten[0]\
        .strip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%()<>br/"))
        self.uploadpercentage   = int(zoekresultaten[1]\
        .strip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%()<>br/"))


        self.balkgetal_download = \
        int(round(float(self.downloadpercentage) / 10.0))
        self.balkgetal_upload = \
        int(round(float(self.uploadpercentage) / 10.0))
        
        ## Balken tekenen in de terminal
        
        if self.downloadpercentage <= 10:
            self.voorwaardelijke_kleur_download = \
            self.co.tekstKleurRoodOpmaakVet
        elif 10 < self.downloadpercentage < 60:
            self.voorwaardelijke_kleur_download = \
            self.co.tekstKleurGeelOpmaakVet
        else:
            self.voorwaardelijke_kleur_download = \
            self.co.tekstKleurGroenOpmaakVet
        
        if self.uploadpercentage <= 10:
            self.voorwaardelijke_kleur_upload = \
            self.co.tekstKleurRoodOpmaakVet
        elif 10 < self.uploadpercentage < 60:
            self.voorwaardelijke_kleur_upload = \
            self.co.tekstKleurGeelOpmaakVet
        else:
            self.voorwaardelijke_kleur_upload = \
            self.co.tekstKleurGroenOpmaakVet
        
        
        
        self.co.kprint(4, 23, " " * (3 - len(str(self.downloadpercentage))) + \
        str(self.downloadpercentage) + \
        "%", self.voorwaardelijke_kleur_download)
        self.co.kprint(5, 23, " " * (3 - len(str(self.uploadpercentage))) + \
        str(self.uploadpercentage) + \
        "%", self.voorwaardelijke_kleur_upload)
    
        self.co.kprint(4, 11, "=" * self.balkgetal_download + \
        " " * (10-self.balkgetal_download), self.voorwaardelijke_kleur_download)
        self.co.kprint(5, 11, "=" * self.balkgetal_upload + \
        " " * (10-self.balkgetal_upload), self.voorwaardelijke_kleur_upload)
        self.co.kprint(5, 28, "")
        
        self.co.beeindig_sessie()
