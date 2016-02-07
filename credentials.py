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
    
    def dummy(self):
        gebruikersnaam = "gebruikersnaam"
        wachtwoord = "wachtwoord"
        return gebruikersnaam, wachtwoord
