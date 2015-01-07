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
import urlparse                         ## Diverse URL-manipulaties
import mechanize                        ## Emuleert een browser
import socket                           ## Voor ophalen IP
import sys                              ## Basislib
import os                               ## Basislib

from tools import pinger                ## Om te checken of we op Kotnet zitten
from tools import errorcodes as error   ## Om magic number errors te voorkomen
from bs4 import BeautifulSoup, Comment  ## Om webinhoud proper te parsen.



class Kotnetlogin():
    def __init__(self, co, gebruikersnaam, wachtwoord, afsluiten=True):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        self.afsluiten = afsluiten
        
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            respons = self.browser.open("https://netlogin.kuleuven.be", \
            timeout=1.8)
            html = respons.read()
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            #sys.exit(1)
            sys.exit(error.NOHOST)
            ## voorbeeld van hoe het er uit moet komen zien
        
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
        
        soup = BeautifulSoup(html)
        
        ## Zoek naar de rc-code in de comments van het html-bestand. Deze
        ## bevat de status.
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        p = re.compile("weblogin: rc=\d+")
        for c in comments:
            m = p.search(c)
            #m = p.findall(c)
            #print m
            if m:
                rccode = int(m.group().strip("weblogin: rc="))
                ## m = p.search(c): zoekt naar de RE p in c. Indien die is
                ## gevonden, is m een object; m.group() geeft vervolgens 
                ## weer waar de RE matcht. Dit doet het maar één keer; als
                ## je strings op meerdere matches wilt controleren, moet je
                ## p.findall(c) gebruiken, zoals hieronder.
        
        if rccode == 100:            
            ## succesvolle login
            ## downloadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[6])
            self.downloadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))
            
            ## uploadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[7])
            self.uploadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))
            
            
            self.co.eventLoginGeslaagd(self.downloadpercentage, \
            self.uploadpercentage)
            
            #self.co.eventSamenvattingGeven("login", True)
            self.co.beeindig_sessie(0)
            return(True)
            
        elif rccode == 202:
            ## verkeerd wachtwoord
            print "Uw logingegevens kloppen niet. Gebruik kotnetcli " + \
            "--forget om deze te resetten."
            self.co.beeindig_sessie(1)
            return(True)
        
        elif rccode == 206:
            ## al ingelogd op ander IP
            print "U bent al ingelogd op een ander IP-adres. Gebruik " + \
            "kotnetcli --force-login om u toch in te loggen." 
            
            self.co.beeindig_sessie(1)
            return(False)
        
        else:
            self.co.beeindig_sessie(1)
            print html
            print "\nrc-code onbekend. Stuur bovenstaande informatie naar"
            print "gijs.timmers@student.kuleuven.be om ondersteuning te krijgen."
            
            return(True)
            
        #print self.afsluiten
        if self.afsluiten:
            self.co.beeindig_sessie()
        
    def uitteloggenipophalen(self):
        html = self.browser.response().read()
        soup = BeautifulSoup(html)
        
        forms = soup.findAll("form")
        form = forms[1]
        uitteloggenip = form.contents[3]["value"]
        
        return uitteloggenip

class Kotnetloguit():
    def __init__(self, co, gebruikersnaam, wachtwoord, uitteloggenip=None, afsluiten=True):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        self.uitteloggenip = uitteloggenip
        self.afsluiten = afsluiten
        
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
        html = self.browser.response().read()
        #print html
        soup = BeautifulSoup(html)
        
        ## Zoek naar de rc-code in de comments van het html-bestand. Deze
        ## bevat de status.
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        p = re.compile("weblogout: rc=\d+")
        
        rccode = 100 
        ## if no error codes appear, assume that everything went OK.
        for c in comments:
            m = p.search(c)
            #m = p.findall(c)
            #print m
            if m:
                rccode = int(m.group().strip("weblogout: rc="))
            
        if rccode == 100:
            ## succesvolle logout
            #self.co.eventSamenvattingGeven("loguit", True)
            self.co.beeindig_sessie(0)
            
        elif rccode == 207:
            ## al uitgelogd
            print "U had uzelf reeds succesvol uitgelogd."
            self.co.beeindig_sessie(0)
            
        else:
            self.co.beeindig_sessie(1)
            print html
        
        
        #print self.afsluiten
        if self.afsluiten:
            self.co.beeindig_sessie()
            ## this should be removed
        
class Dummylogin():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        
    def netlogin(self):
        self.co.eventNetloginStart()
        try:
            time.sleep(0.1)
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            sys.exit(1)
        
    def kuleuven(self):
        self.co.eventKuleuvenStart()
        try:
            time.sleep(0.1)
            self.co.eventKuleuvenSuccess()
        except:
            self.co.eventKuleuvenFailure()
            sys.exit(1)

    def gegevensinvoeren(self):
        self.co.eventInvoerenStart()
        try:
            time.sleep(0.1)
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            sys.exit(1)
        
        
    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            time.sleep(0.1)
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            sys.exit(1)
        
        
    def tegoeden(self):
        self.downloadpercentage = 10
        self.uploadpercentage   = 59
        
        self.co.eventLoginGeslaagd(self.downloadpercentage, \
        self.uploadpercentage)
        
        self.co.beeindig_sessie(0)

class Dummyloguit():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        
        self.lokaleip = "192.168.1.1"
        
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
            time.sleep(0.1)
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
            time.sleep(0.1)
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            sys.exit(1)
    
    def gegevensopsturen(self):
        self.co.eventOpsturenStart()
        try:
            time.sleep(0.1)
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            sys.exit(1)
    
    def tegoeden(self):
        self.co.beeindig_sessie(0)
