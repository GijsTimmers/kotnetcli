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

#import re                               ## Basislib voor reguliere expressies
#import time                             ## Voor timeout om venster te sluiten
import sys                              ## for advanced print functions
#import os                               ## Basislib
#import platform                         ## Om onderscheid Lin/Mac te maken
from quietc import QuietCommunicator
#from ..tools import cursor              ## Om cursor te verbergen/tonen
from tools import cursor                ## Om cursor te verbergen/tonen

## Gijs:
## We hoeven geen relatieve import te gebruiken omdat de map waarin 
## kotnetcli.py zich bevindt de rootmap ($PYTHONPATH) is. De map 'tools'
## bevindt zich daar ook; daarom hoeven we niet te verwijzen naar de lokatie
## ten opzichte van deze specifieke communicator (denk ik)

class SuperPlaintextCommunicator(QuietCommunicator):
    def __init__(self):
        cursor.hide()

    #### 1. appearance printing methods ####

    ## Encapsulates the printing of an error string on stderr
    ## Override this method to change the appearance of the printed string.
    def printerr(self, msg):
        sys.stderr.write(msg),
        sys.stderr.flush()

    ## Encapsulates the printing of a "text" string on stdout, *without* a trailing newline
    ## Override this method to change the appearance of the printed string.
    def print_txt(self, msg):
        sys.stdout.write(msg)

    ## Encapsulates the printing of a "wait" event on stdout
    ## Override this method to change the appearance of the printed string.
    def print_wait(self, msg):
        print msg + "[WAIT]" + "\b\b\b\b\b\b\b",
        sys.stdout.flush()

    ## Encapsulates the printing of a "succes" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_success(self):
        print "[ OK ]"

    ## Encapsulates the printing of a "done" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_done(self):
        print "[DONE]"

    ## Encapsulates the printing of a "fail" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_fail(self):
        print "[ FAIL ]"

    ## generic print_balk method (not meant to be overriden)
    def print_generic_balk(self, percentage, style, color, stop_color, stop_style):
        
        percentagefloat = float(percentage)
        percentagestring = str(percentage)
        
        lengteVanBalkfloat = 10.0
        lengteVanBalkint = 10
        lengteVanRuimteVoorPercentages = 3
        
        aantalStreepjesObvPercentage = int(round(percentagefloat/lengteVanBalkfloat))
        print style + "[" + color + \
        "=" * aantalStreepjesObvPercentage + stop_color + \
        " " * (lengteVanBalkint-aantalStreepjesObvPercentage) + \
        "][" + \
        " " * (lengteVanRuimteVoorPercentages - len(percentagestring)) + \
        color + percentagestring + "%" + \
        stop_color + "]" + stop_style

    ## Encapsulates the printing of a "balk" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_balk(self, percentage):
        self.print_generic_balk(percentage, "", "", "", "")

    #### 2. communicator method implementations common for both login and logout ####

    #def eventPingFailure(self):
    #    self.printerr("Niet verbonden met het KU Leuven-netwerk.")
    #    
    #def eventPingAlreadyOnline(self):
    #    self.printerr("U bent al online.")

    def eventKotnetVerbindingStart(self):
        self.print_wait("Kotnet verbinding testen... ")
        
    def eventKotnetVerbindingSuccess(self):
        self.print_success()
    
    def eventKotnetVerbindingFailure(self):
        self.print_fail()

    def eventNetloginSuccess(self):
        self.print_success()
    def eventNetloginFailure(self):
        self.print_fail()
        
    def eventKuleuvenStart(self):
        self.print_wait("KU Leuven kiezen........... ")
    def eventKuleuvenSuccess(self):
        self.print_success()
    def eventKuleuvenFailure(self):
        self.print_fail()

    def eventInvoerenStart(self):
        self.print_wait("Gegevens invoeren.......... ")
    def eventInvoerenSuccess(self):
        self.print_success()
    def eventInvoerenFailure(self):
        self.print_fail()

    def eventOpsturenStart(self):
        self.print_wait("Gegevens opsturen.......... ")
    def eventOpsturenSuccess(self):
        self.print_success()
    def eventOpsturenFailure(self):
        self.print_fail()
    
class LoginPlaintextCommunicator(SuperPlaintextCommunicator):     
    def eventNetloginStart(self):
        ## TODO: jo : inloggen is al duidelijk door "netLOGIN" right?
        ## Gijs: Zie noot bij LogoutPlaintextCommunicator.eventNetloginStart().
        
        #print "           Inloggen           "
        #print "------------------------------"
        
        
        self.print_wait("Netlogin openen............ ")

    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        self.print_txt("Download:       ")
        self.print_balk(downloadpercentage)
        self.print_txt("Upload:         ")
        self.print_balk(uploadpercentage)
        
    def beeindig_sessie(self, error_code=0):
        self.print_txt("Inloggen................... "),
        if error_code == 0:
            self.print_done()
        else:
            self.print_fail()
        cursor.show()

class LogoutPlaintextCommunicator(SuperPlaintextCommunicator):
    def eventNetloginStart(self):
        ## TODO jo : "netLOGOUT" duidelijk genoeg?
        ##
        ## Gijs: Mijn voorkeur gaat uit naar een header:
        ##       - Een header is duidelijker, zeker met het oog op
        ##         --force-login, in dat geval zal er eerst een Uitloggen-header
        ##         zijn en daarna een Inloggen-header
        ##       - "Formulier aanmaken" is een betere beschrijving van wat er
        ##         gebeurt
        ##
        ##       Eventueel kunnen we een nieuwe methode maken, bijvoorbeeld
        ##       headerAanmaken(). In dat geval kan de header zijn:
        ##       "Geforceerd inloggen" of iets dergelijks. Ook leuk!
        
        print "          Uitloggen           "
        print "------------------------------"
        
        
        #print "Formulier openen....... " + Style.BRIGHT + "[" + Fore.YELLOW + \
        #"WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        #sys.stdout.flush()
        
        self.print_wait("Netlogout openen....... ")


    ## TODO: jo wat is nog het nut van "eventLogoutGeslaagd"??
    ## dit kan ook in beendig_sessie right?
    ## Gijs: Kan inderdaad ook in beeindig_sessie(). Mijn voorkeur gaat er naar
    ##       uit om een aparte methode aan te maken, eventLoginGeslaagd() en 
    ##       eventLogoutGeslaagd(). De reden hiervoor is dat een geslaagde
    ##       logout niet noodzakelijk het einde van een sessie aangeeft. Bij-
    ##       voorbeeld, in --force-login moet er na het uitloggen opnieuw wor-
    ##       den ingelogd. Het is dan vreemd, om de sessie eerst af te sluiten,
    ##       met alle gevolgen van dien (hier: cursor tonen, bij curses:
    ##       scherm afsluiten). Dat zou betekenen dat bij --force-login na het
    ##       uitloggen de cursor zichtbaar wordt, en dan opnieuw verdwijnt.\
    ##  
    ##       Daarnaast was het mijn plan om de sys.exit() in de communicator
    ##       te zetten, maar misschien kunnen we deze beter in de worker plaat-
    ##       sen.
    
    def eventLogoutGeslaagd(self):
        pass

    def beeindig_sessie(self, error_code=0):
        self.print_txt("Uitloggen............. "),
        if error_code == 0:
            self.print_success()
        else:
            self.print_fail()
        cursor.show()

