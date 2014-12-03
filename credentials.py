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

import keyring                          ## Voor ophalen wachtwoord
import getpass                          ## Voor invoer wachtwoord zonder print

class Credentials():
    def getset(self):
        if (keyring.get_password("kotnetcli", "gebruikersnaam") == None) or\
        (keyring.get_password("kotnetcli", "wachtwoord") == None):
            gebruikersnaam = raw_input("Voer uw s-nummer/r-nummer in... ")
            wachtwoord = getpass.getpass(prompt="Voer uw wachtwoord in... ")
            
            keyring.set_password("kotnetcli", "gebruikersnaam", gebruikersnaam)
            keyring.set_password("kotnetcli", "wachtwoord", wachtwoord)
        
        gebruikersnaam = keyring.get_password("kotnetcli", "gebruikersnaam")
        wachtwoord = keyring.get_password("kotnetcli", "wachtwoord")
        return gebruikersnaam, wachtwoord
    
    def forget(self):
        try:                
            keyring.delete_password("kotnetcli", "gebruikersnaam")
            keyring.delete_password("kotnetcli", "wachtwoord")
            print "You have succesfully removed your kotnetcli credentials."
        except keyring.errors.PasswordDeleteError:
            print "You have already removed your kotnetcli credentials."
    
    def guest(self):
        gebruikersnaam = raw_input("Voer uw s-nummer/r-nummer in... ")
        wachtwoord = getpass.getpass(prompt="Voer uw wachtwoord in... ")
        return gebruikersnaam, wachtwoord
