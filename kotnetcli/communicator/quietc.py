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

class QuietCommunicator():
    def __init__(self):
        pass

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
        pass

    ## Encapsulates the printing of a "succes" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_success(self):
        pass

    ## Encapsulates the printing of a "done" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_done(self):
        pass

    ## Encapsulates the printing of a "fail" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_fail(self):
        pass

    ## generic print_balk method (not meant to be overriden)
    def print_generic_balk(self, percentage, style, color, stop_color, stop_style):
        pass

    ## Encapsulates the printing of a "balk" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_balk(self, percentage):
        pass

    #### 2. communicator method implementations common for both login and logout ####

    #def eventPingFailure(self):
    #    self.printerr("Niet verbonden met het KU Leuven-netwerk.")
    #    
    #def eventPingAlreadyOnline(self):
    #    self.printerr("U bent al online.")

    def eventKotnetVerbindingStart(self):
        pass
        
    def eventKotnetVerbindingSuccess(self):
        pass
    
    def eventKotnetVerbindingFailure(self):
        pass

    def eventNetloginStart(self):
        pass
    def eventNetloginSuccess(self):
        pass
    def eventNetloginFailure(self):
        pass
        
    def eventKuleuvenStart(self):
        pass
    def eventKuleuvenSuccess(self):
        pass
    def eventKuleuvenFailure(self):
        pass

    def eventInvoerenStart(self):
        pass
    def eventInvoerenSuccess(self):
        pass
    def eventInvoerenFailure(self):
        pass

    def eventOpsturenStart(self):
        pass
    def eventOpsturenSuccess(self):
        pass
    def eventOpsturenFailure(self):
        pass


    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        pass
    def eventLogoutGeslaagd(self):
        pass
        
    def beeindig_sessie(self, error_code=0):
        pass



"""
class SuperQuietCommunicator():
    def __init__(self):
        pass

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
        pass

    ## Encapsulates the printing of a "succes" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_success(self):
        pass

    ## Encapsulates the printing of a "done" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_done(self):
        pass

    ## Encapsulates the printing of a "fail" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_fail(self):
        pass

    ## generic print_balk method (not meant to be overriden)
    def print_generic_balk(self, percentage, style, color, stop_color, stop_style):
        pass

    ## Encapsulates the printing of a "balk" string on stdout
    ## Override this method to change the appearance of the printed string.
    def print_balk(self, percentage):
        pass

    #### 2. communicator method implementations common for both login and logout ####

    #def eventPingFailure(self):
    #    self.printerr("Niet verbonden met het KU Leuven-netwerk.")
    #    
    #def eventPingAlreadyOnline(self):
    #    self.printerr("U bent al online.")

    def eventKotnetVerbindingStart(self):
        pass
        
    def eventKotnetVerbindingSuccess(self):
        pass
    
    def eventKotnetVerbindingFailure(self):
        pass

    def eventNetloginSuccess(self):
        pass
    def eventNetloginFailure(self):
        pass
        
    def eventKuleuvenStart(self):
        pass
    def eventKuleuvenSuccess(self):
        pass
    def eventKuleuvenFailure(self):
        pass

    def eventInvoerenStart(self):
        pass
    def eventInvoerenSuccess(self):
        pass
    def eventInvoerenFailure(self):
        pass

    def eventOpsturenStart(self):
        pass
    def eventOpsturenSuccess(self):
        pass
    def eventOpsturenFailure(self):
        pass

class LoginQuietCommunicator(SuperQuietCommunicator):
    def eventNetloginStart(self):
        pass

    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        pass
        
    def beeindig_sessie(self, error_code=0):
        pass

class QuietLogoutCommunicator(SuperQuietCommunicator):
    def eventNetloginStart(self):
        pass

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
        pass

"""