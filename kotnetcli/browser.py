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

import logging
logger = logging.getLogger(__name__)

## the maximum waiting time in seconds for browser connections
BROWSER_TIMEOUT_SEC = 1.5

## the part of the login url before the institution choice
NETLOGIN_URL_PART_1 = "https://netlogin.kuleuven.be/cgi-bin/wayf2.pl?inst="
## the part of the login url after the institution choice
NETLOGIN_URL_PART_2 = "&lang=nl&submit=Ga+verder+%2F+Continue"

## login rc codes contained in the response html page
RC_LOGIN_SUCCESS            = 100
RC_LOGIN_INVALID_USERNAME   = 201
RC_LOGIN_INVALID_PASSWORD   = 202
RC_LOGIN_MAX_IP             = 206
RC_INVALID_INSTITUTION      = 211
RC_INTERNAL_SCRIPT_ERR      = 301

## custom exceptions
class WrongCredentialsException(Exception):
    pass

class InternalScriptErrorException(Exception):
    pass

class InvalidInstitutionException(Exception):
    def __init__(self, inst):
        self.inst = inst
    
    def get_inst(self):
        return self.inst

##TODO hier het ip address in opslaan (~ hieronder de rccode)
class MaxNumberIPException(Exception):
    pass
    
class UnknownRCException(Exception):
    def __init__(self, rccode, html):
        self.rccode = rccode
        self.html = html

    def get_info(self):
        return (self.rccode, self.html)

## The class doing the actual browser emulation work. One can extend this
## class to add specific behavior (e.g. communicating; err catching; etc).
## KotnetBrowser() is like an API: it contains all possible Browser operations.
## So, we don't create a LoginBrowser(), LogoutBrowser(), etc. Instead, the
## proper Worker() is instantiated by kotnetcli.py, and this instance calls
## only the Browser() methods that it needs.
## Some 
class KotnetBrowser():
     
    ## Note: the browser itself doesn't save any credentials. These are kept in a
    ## credentials object that is supplied when needed
    def __init__(self, inst):
        self.institution = inst
        self.netlogin_url = NETLOGIN_URL_PART_1 + inst + NETLOGIN_URL_PART_2
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
    
    ## returns True | False depending on whether or not the user seems to be on the
    ## kotnet network (connect to  netlogin.kuleuven.be)
    def bevestig_kotnetverbinding(self):
        ## try to open a TCP connection on port 443 with a maximum waiting time
        try:
            sock = socket.create_connection(("netlogin.kuleuven.be", 443), BROWSER_TIMEOUT_SEC)
            sock.close()
            return True
        except socket.error:
            ## note: socket.timeout, socket.gaierror and socket.herror seem to be subclasses of socket.error
            return False
    
    def login_open_netlogin(self):
        response = self.browser.open(self.netlogin_url, \
        timeout=BROWSER_TIMEOUT_SEC)
        #html = response.read()

    #def login_kies_kuleuven(self):
    #    self.browser.select_form(nr=1)
    #    self.browser.submit()
    
    def login_input_credentials(self, creds):
        (gebruikersnaam, wachtwoord) = creds.getCreds()
        self.browser.select_form(nr=1)
        self.browser.form["uid"] = gebruikersnaam
        wachtwoordvaknaam = \
        self.browser.form.find_control(type="password").name
        self.browser.form[wachtwoordvaknaam] = wachtwoord
    
    def login_send_credentials(self):
        self.browser.submit()

    ## This method parses the server's response. On success, it returns a tuple of
    ## length 2: (downloadpercentage, uploadpercentage); else it raises an
    ## appropriate exception
    def login_parse_results(self):
        html = self.browser.response().read()

        soup = BeautifulSoup(html, "lxml")

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

        logger.debug("rccode is %s", rccode)

        if rccode == RC_LOGIN_SUCCESS:
            ## downloadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[6])
            downloadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            ## uploadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[7])
            uploadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            return (downloadpercentage, uploadpercentage)

        elif (rccode == RC_LOGIN_INVALID_USERNAME) or \
            (rccode == RC_LOGIN_INVALID_PASSWORD):
            raise WrongCredentialsException()
            
        elif rccode == RC_LOGIN_MAX_IP:
            raise MaxNumberIPException()

        elif rccode == RC_INVALID_INSTITUTION:
            raise InvalidInstitutionException(self.institution)
        
        elif self.rccode == RC_INTERNAL_SCRIPT_ERR:
            raise InternalScriptErrorException()

        else:
            raise UnknownRCException(rccode, html)
    
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
    ## allow custom test behavior via params
    def __init__(self, inst, dummy_timeout, kotnet_online, netlogin_unavailable, rccode, downl, upl):
        self.institution = inst
        self.dummy_timeout = dummy_timeout
        self.kotnet_online=kotnet_online
        self.netlogin_unavailable = netlogin_unavailable
        self.rccode = rccode
        self.download = abs(downl) %101
        self.upload = abs(upl) %101
    
    def bevestig_kotnetverbinding(self):
        return self.kotnet_online

    def login_open_netlogin(self):
        if (not self.netlogin_unavailable):
            time.sleep(self.dummy_timeout)
        else:
            raise Exception

    #def login_kies_kuleuven(self):
    #    time.sleep(0.1)
    
    def login_input_credentials(self, creds):
        time.sleep(self.dummy_timeout)

    def login_send_credentials(self):
        time.sleep(self.dummy_timeout)

    def login_parse_results(self):
        logger.debug("rccode is %s", self.rccode)
        
        if self.rccode == RC_LOGIN_SUCCESS:
            return (self.download, self.upload)

        elif (self.rccode == RC_LOGIN_INVALID_PASSWORD) or \
            (self.rccode == RC_LOGIN_INVALID_USERNAME):
            raise WrongCredentialsException()
            
        elif self.rccode == RC_LOGIN_MAX_IP:
            raise MaxNumberIPException()

        elif self.rccode == RC_INVALID_INSTITUTION:
            raise InvalidInstitutionException(self.institution)
        
        elif self.rccode == RC_INTERNAL_SCRIPT_ERR:
            raise InternalScriptErrorException()

        else:
            raise UnknownRCException(self.rccode, "\n<html>\n<p>the dummy html page</p>\n</html>\n")


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
