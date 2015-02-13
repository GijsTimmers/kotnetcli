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

import keyring                          ## Voor ophalen wachtwoord

class ForgetCredsException(Exception):
    pass

## a credentials implementation saving the credentials in the OS keyring
## note: all user feedback should happen in the front-end (kotnetcli.py)
class KeyRingCredentials():
    def __init__(self):
        self.kr = keyring.get_keyring()

    def hasCreds(self):
        return not ((self.kr.get_password("kotnetcli", "gebruikersnaam") == None) or\
            (self.kr.get_password("kotnetcli", "wachtwoord") == None))
    
    def getCreds(self):
        gebruikersnaam = self.kr.get_password("kotnetcli", "gebruikersnaam")
        wachtwoord = self.kr.get_password("kotnetcli", "wachtwoord")
        return (gebruikersnaam, wachtwoord)
    
    def saveCreds(self, gebruikersnaam, wachtwoord):
        self.kr.set_password("kotnetcli", "gebruikersnaam", gebruikersnaam)
        self.kr.set_password("kotnetcli", "wachtwoord", wachtwoord)
    
    def forgetCreds(self):
        try:
            self.kr.delete_password("kotnetcli", "gebruikersnaam")
            self.kr.delete_password("kotnetcli", "wachtwoord")
        except keyring.errors.PasswordDeleteError:
            raise ForgetCredsException()

'''
class GuestCredentials():
    def hasCreds
    
    def getCreds
    
    def saveCreds
    
    def forgetCred
'''

class DummyCredentials():
    def __init__(self):
        self.user = "dummy_user"
        self.password = "dummy_password"

    def hasCreds(self):
        return True
    
    def getCreds(self):
        return (self.user, self.password)
    
    def saveCreds(self, gebruikersnaam, wachtwoord):
        self.user = gebruikersnaam
        self.password = wachtwoord
    
    def forgetCreds(self):
        self.user = "None (deleted)"
        self.password = "None (deleted)"
