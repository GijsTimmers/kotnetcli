#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-keyring
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

import keyring                          ## Voor ophalen wachtwoord
import time                             ## Voor timeout

def vergeetCredentials():
    kr = keyring.get_keyring()
    try:
        kr.delete_password("kotnetcli", "gebruikersnaam")
        kr.delete_password("kotnetcli", "wachtwoord")
        print "---------------------------------------------"
        print "Kotnetcli-logingegevens succesvol verwijderd!"
        print "---------------------------------------------"
    except keyring.errors.PasswordDeleteError:
        print "-------------------------------------------"
        print "Kotnetcli-logingegevens zijn al verwijderd!"
        print "-------------------------------------------"
    finally:
        time.sleep(3)
        

if __name__ == '__main__':
    vergeetCredentials()

