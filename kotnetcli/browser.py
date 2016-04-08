#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck
##
## Licence:         GPLv3
##
## kotnetcli is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## kotnetcli is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with kotnetcli.  If not, see <http://www.gnu.org/licenses/>.

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import urlparse                         ## Diverse URL-manipulaties
import requests                         ## Invullen van HTTP POST-request
import socket                           ## Voor ophalen IP
import os                               ## Basislib

from bs4 import BeautifulSoup, Comment  ## Om webinhoud proper te parsen.

## login rc codes contained in the response html page
import server.rccodes

import logging
logger = logging.getLogger(__name__)

NETLOGIN_HOST       = "netlogin.kuleuven.be"
NETLOGIN_PORT       = 443

#FIXME ensure the custom certificate is only used for the test server
CERT_FILE           = 'kotnetcli/server/kotnetcli-localhost.pem'

## the maximum waiting time in seconds for browser connections
BROWSER_TIMEOUT_SEC = 1.5

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
class KotnetBrowser(object):
     
    ## Note: the browser itself doesn't save any credentials. These are kept in a
    ## credentials object that is supplied when needed
    def __init__(self, inst, host=NETLOGIN_HOST, port=NETLOGIN_PORT):
        self.institution = inst
        self.language = "nl"
        self.host = host
        self.port = port
        
        ## What the user sees when using netlogin. We need this url to
        ## find the password field name ("pwdXXXXX")
        self.html_get_url = "https://{}:{}/cgi-bin/wayf2.pl?inst={}&lang=nl&submit=Ga+verder+%2F+Continue".format(self.host, self.port, self.institution)
        
        ## The backend: contains the to-be-submitted form.
        self.html_post_url = "https://{}:{}/cgi-bin/netlogin.pl".format(self.host, self.port)

    ## returns True | False depending on whether or not the user seems to be on the
    ## kotnet network (connect to  netlogin.kuleuven.be)
    def bevestig_kotnetverbinding(self):
        ## try to open a TCP connection on port 443 with a maximum waiting time
        try:
            sock = socket.create_connection((self.host,self.port), BROWSER_TIMEOUT_SEC)
            sock.close()
            return True
        except socket.error:
            ## note: socket.timeout, socket.gaierror and socket.herror seem to be subclasses of socket.error
            return False
    
    def login_open_netlogin(self):
        ## Voorstel: vervangen door "Onderzoekt HTML..." (dwz zoekt wachtwoordvaknaam op)
        ## of: verwijder in zijn geheel. Is alleen interessant om de legacy
        ## kotnetcli-werkingen te tonen, heeft nauwelijks nog relevantie voor
        ## de huidige codebase. Het opzoeken van het wachtwoordvak kan
        ## haast net zo goed in login_input_credentials() worden gezet.

        #FIXME ensure the custom certificate is only used for the test server
        r = requests.get(self.html_get_url,verify=CERT_FILE)
        logger.debug("HTTP GET RESPONSE FROM SERVER is:\n\n%s\n" % r.text)
        # search for something of the form name="pwd123" and extract the pwd123 part
        self.wachtwoordvak = re.findall("(?<=name=\")pwd\d*", r.text).pop()
        
    def login_input_credentials(self, creds):
        (gebruikersnaam, wachtwoord) = creds.getCreds()
        
        self.payload = {
            "inst": self.institution,
            "lang": self.language,
            "submit": "Login",
            "uid": gebruikersnaam,
            self.wachtwoordvak: wachtwoord        
        }
    
    def login_send_credentials(self):
        #FIXME ensure the custom certificate is only used for the test server
        r = requests.post(self.html_post_url, data=self.payload, verify=CERT_FILE)
        logger.debug("HTTP POST RESPONSE FROM SERVER is:\n\n%s\n" % r.text)
        self.html = r.text

    ## This method parses the server's response. On success, it returns a tuple of
    ## length 2: (downloadpercentage, uploadpercentage); else it raises an
    ## appropriate exception
    def login_parse_results(self):
        #soup = BeautifulSoup(self.html, "lxml")
        soup = BeautifulSoup(self.html, "html.parser")   
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

        if rccode == server.rccodes.RC_LOGIN_SUCCESS:
            ## downloadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[6])
            downloadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            ## uploadpercentage parsen
            p = re.compile("\d+")
            m = p.findall(comments[7])
            uploadpercentage = int(round(float(m[0]) / float(m[1]) * 100, 0))

            return (downloadpercentage, uploadpercentage)

        elif (rccode == server.rccodes.RC_LOGIN_INVALID_USERNAME) or \
            (rccode == server.rccodes.RC_LOGIN_INVALID_PASSWORD):
            raise WrongCredentialsException()
            
        elif rccode == server.rccodes.RC_LOGIN_MAX_IP:
            raise MaxNumberIPException()

        elif rccode == server.rccodes.RC_INVALID_INSTITUTION:
            raise InvalidInstitutionException(self.institution)
        
        elif self.rccode == server.rccodes.RC_INTERNAL_SCRIPT_ERR:
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
        
        with open("tools/logoutformuliertemplate.html", "r") as logoutformulier_in:
            data = logoutformulier_in.read()
            data = data.format(**gegevens) ## gegevens worden hier ingevuld
        with open("tools/logoutformulieringevuld.html", "w") as logoutformulier_out:
            logoutformulier_out.write(data)
        
        self.url_logoutformulier = urlparse.urljoin("file:", \
        os.path.abspath("tools/logoutformulieringevuld.html"))
    
    def logout_send_credentials(self):
        self.browser.open(self.url_logoutformulier, timeout=1.8)
        self.browser.select_form(nr=0)
        self.browser.submit()
        os.remove("tools/logoutformulieringevuld.html")
    
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

class DummyBrowser(object):
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
    
    def login_input_credentials(self, *args):
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


"""
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
"""
