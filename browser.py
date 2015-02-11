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

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import urllib                           ## Diverse URL-manipulaties
import urlparse                         ## Diverse URL-manipulaties
import mechanize                        ## Emuleert een browser
import socket                           ## Voor ophalen IP
import sys                              ## Basislib
import os                               ## Basislib

from bs4 import BeautifulSoup, Comment  ## Om webinhoud proper te parsen.

## The class doing the actual browser emulation work. One can extend this
## class to add specific behavior (e.g. communicating; err catching; etc).
## KotnetBrowser() is like an API: it contains all possible Browser operations.
## So, we don't create a LoginBrowser(), LogoutBrowser(), etc. Instead, the
## proper Worker() is instantiated by kotnetcli.py, and this instance calls
## only the Browser() methods that it needs.
## Some 

class KotnetBrowser():
    def __init__(self, gebruikersnaam, wachtwoord):
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        self.gebruikersnaam = gebruikersnaam    #TODO niet opslaan...
        self.wachtwoord = wachtwoord
    
    ## returns True | False depending on whether or not the user seems to be on the
    ## kotnet network (connect to  netlogin.kuleuven.be)
    def bevestig_kotnetverbinding():
        ## try to open a TCP connection on port 443 with a timeout of 1.5 second
        try:
            sock = socket.create_connection(("netlogin.kuleuven.be", 443), 1.5)
            sock.close()
            return True
        except:
            return False
    
    def login_open_netlogin(self):
        response = self.browser.open("https://netlogin.kuleuven.be", \
        timeout=1.8)
        #html = response.read()

    def login_kies_kuleuven(self):
        self.browser.select_form(nr=1)
        self.browser.submit()
    
    def login_input_credentials(self):
        self.browser.select_form(nr=1)
        self.browser.form["uid"] = self.gebruikersnaam
        wachtwoordvaknaam = \
        self.browser.form.find_control(type="password").name
        self.browser.form[wachtwoordvaknaam] = self.wachtwoord

    def login_send_credentials(self):
        self.browser.submit()

    ## This method parses the server's response. On success, it returns a tuple of
    ## length 2: (downloadpercentage, uploadpercentage); else this method
    ## returns a tuple of length 1, containing a descriptive errmsg
    ## TODO vervang magic tuple len 1 met errmsg door gerichte exception of gewoon errcode?
    def login_parse_results(self):
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
            downloadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            ## uploadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[7])
            uploadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            return (downloadpercentage, uploadpercentage)

        elif rccode == 202:
            ## verkeerd wachtwoord
            return("Uw logingegevens kloppen niet. Gebruik kotnetcli " + \
            "--forget om deze te resetten.",)

        elif rccode == 206:
            ## al ingelogd op ander IP
            return ("U bent al ingelogd op een ander IP-adres. Gebruik " + \
            "kotnetcli --force-login om u toch in te loggen.",)

        else:
            print html
            return ("\nrc-code onbekend. Stuur bovenstaande informatie naar \
            gijs.timmers@student.kuleuven.be om ondersteuning te krijgen.",)
    
    def logout_input_credentials(self):
        ## Lokale IP ophalen: lelijk, maar werkt goed en is snel. Is waar-
        ## schijnlijk de kortste code die crossplatform werkt, wat op zich
        ## wel vreemd is. Meer informatie:        
        ## http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        self.uitteloggenip = s.getsockname()[0]
        s.close()
        
        ## Logoutformulier aanmaken, dan lokatie omvormen tot file://-URL zodat
        ## het browserobject hem kan gebruiken als lokatie.
        gegevens = {"uitteloggenip" : self.uitteloggenip, 
                    "gebruikersnaam": self.gebruikersnaam}
        
        with open("logoutformuliertemplate.html", "r") as logoutformulier_in:
            data = logoutformulier_in.read()
            data = data.format(**gegevens) ## gegevens worden hier ingevuld
        with open("logoutformulieringevuld.html", "w") as logoutformulier_out:
            logoutformulier_out.write(data)
        
        self.url_logoutformulier = urlparse.urljoin("file:", \
        os.path.abspath("logoutformulieringevuld.html"))
    
    def logout_send_credentials(self):
        self.browser.open(self.url_logoutformulier, timeout=1.8)
        self.browser.select_form(nr=0)
        self.browser.submit()
        os.remove("logoutformulieringevuld.html")
    
    ## returns True if logout is succesful; False when it fails
    def logout_parse_results(self):
        html = self.browser.response().read()
        soup = BeautifulSoup(html)

        ## Zoek naar de rc-code in de comments van het html-bestand. Deze
        ## bevat de status.
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        p = re.compile("weblogout: rc=\d+")

        rccode = 100
        ## if not error codes appear, assume that everything went OK.
        for c in comments:
            m = p.search(c)
            #m = p.findall(c)
            #print m
            if m:
                rccode = int(m.group().strip("weblogout: rc="))

        if rccode == 100:
            ## succesvolle logout
            return True

        elif rccode == 207:
            ## al uitgelogd
            print "U had uzelf reeds succesvol uitgelogd."
            return False
        else:
            print html

class DummyBrowser():
    def __init__(self):
        pass
    
    def bevestig_kotnetverbinding(self):
        return True

    def login_open_netlogin(self):
        time.sleep(0.1)

    def login_kies_kuleuven(self):
        time.sleep(0.1)
    
    def login_input_credentials(self, creds):
        time.sleep(0.1)

    def login_send_credentials(self):
        time.sleep(0.1)

    ## This method parses the server's response. On success, it returns a tuple of
    ## length 2: (downloadpercentage, uploadpercentage); else this method
    ## returns a tuple of length 1, containing a descriptive errmsg
    def login_parse_results(self):
        return (80, 100)


'''    
## Deze klasse bevat functies voor de forceer-loginmethode. Gaan we nu nog
## niet gebruiken. Deze klasse wordt later waarschijnlijk samengevoegd met
## KotnetBrowser().
class KotnetForceerBrowser(KotnetBrowser):
    def __init__():
        pass
    
    def uitteloggenipophalen(self):
        html = self.browser.response().read()
        soup = BeautifulSoup(html)

        forms = soup.findAll("form")
        form = forms[1]
        uitteloggenip = form.contents[3]["value"]

        return uitteloggenip    
'''
