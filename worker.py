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
        
    
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            respons = self.browser.open("https://netlogin.kuleuven.be", \
            timeout=1.8)
            html = respons.read()
            self.co.eventNetloginSuccess()
            #self.co.kprint(0, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            #self.co.kprint(1, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
        except:
            self.co.eventNetloginFailure()
            #self.co.kprint(0, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            sys.exit(1)
        
    def kuleuven(self):
        self.co.eventKuleuvenStart()
        try:
            self.browser.select_form(nr=1)
            self.browser.submit()
            self.co.eventKuleuvenSuccess()
            #self.co.kprint(1, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            #self.co.kprint(2, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
        except:
            self.co.eventKuleuvenFailure()
            #self.co.kprint(1, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
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
            #self.co.kprint(2, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            #self.co.kprint(3, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            #self.co.kprint(4, 14, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            #self.co.kprint(4, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            #self.co.kprint(5, 14, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            #self.co.kprint(5, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
        except:
            self.co.eventInvoerenFailure()
            #self.co.kprint(2, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            sys.exit(1)
        
        
    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            self.browser.submit()
            self.co.eventOpsturenSuccess()
            #self.co.kprint(3, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
        except:
            self.co.eventOpsturenFailure()
            #self.co.kprint(3, 23, "FAIL", self.co.tekstKleurGeelOpmaakVet) 
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
        
        self.co.eventDownloadtegoedBekend(self.downloadpercentage)
        self.co.eventUploadtegoedBekend(self.uploadpercentage)

        self.co.beeindig_sessie()
