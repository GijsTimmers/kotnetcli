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

class ForgetCredsException(Exception):
    pass

## a credentials implementation saving the credentials in the OS keyring
## note: all user feedback should happen in the front-end (kotnetcli.py)
## "guest creds" are saved locally and thus forgot after object destruction
class KeyRingCredentials(object):
    def __init__(self):
        self.kr = keyring.get_keyring()
        self.guest_user = None
        self.guest_password = None

    def hasCreds(self):
        return not ((self.kr.get_password("kotnetcli", "gebruikersnaam") == None) or\
            (self.kr.get_password("kotnetcli", "wachtwoord") == None))
    
    def hasGuest(self):
        return not ((self.guest_user == None) or (self.guest_password == None))
    
    def getCreds(self):
        if (self.hasGuest()):
            gebruikersnaam = self.guest_user
            wachtwoord = self.guest_password
        else:
            gebruikersnaam = self.kr.get_password("kotnetcli", "gebruikersnaam")
            wachtwoord = self.kr.get_password("kotnetcli", "wachtwoord")
        return (gebruikersnaam, wachtwoord)
    
    def saveCreds(self, gebruikersnaam, wachtwoord):
        self.kr.set_password("kotnetcli", "gebruikersnaam", gebruikersnaam)
        self.kr.set_password("kotnetcli", "wachtwoord", wachtwoord)
    
    def saveGuestCreds(self, gebruikersnaam, wachtwoord):
        self.guest_user = gebruikersnaam
        self.guest_password = wachtwoord

    def forgetCreds(self):
        try:
            self.kr.delete_password("kotnetcli", "gebruikersnaam")
            self.kr.delete_password("kotnetcli", "wachtwoord")
        except keyring.errors.PasswordDeleteError:
            raise ForgetCredsException()

class DummyCredentials(object):
    def __init__(self):
        self.user = "dummy_user"
        self.password = "dummy_password"
        self.guest_user = None
        self.guest_password = None

    def hasCreds(self):
        return True
    
    def hasGuest(self):
        return not ((self.guest_user == None) or (self.guest_password == None))
    
    def getCreds(self):
        if self.hasGuest():
            return (self.guest_user, self.guest_password)
        else:
            return (self.user, self.password)
    
    def saveCreds(self, gebruikersnaam, wachtwoord):
        self.user = gebruikersnaam
        self.password = wachtwoord
    
    def saveGuestCreds(self, gebruikersnaam, wachtwoord):
        self.guest_user = gebruikersnaam
        self.guest_password = wachtwoord

    def forgetCreds(self):
        self.user = "None (deleted)"
        self.password = "None (deleted)"
