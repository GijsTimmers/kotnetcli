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

class AbstractCredentials(object):
    def hasCreds(self):
        return False
    
    def forgetCreds(self):
        pass #raise ForgetCredsException

class GuestCredentials(AbstractCredentials):
    def __init__(self):
        self.user = None
        self.password = None
        
    def hasCreds(self):
        return not (self.user is None or self.password is None)
    
    def getCreds(self):
        return (self.user, self.password)

    def saveCreds(self, gebruikersnaam, wachtwoord):
        self.user = gebruikersnaam
        self.password = wachtwoord

class DummyCredentials(GuestCredentials):
    def __init__(self):
        self.user = "dummy_user"
        self.password = "dummy_password"

class ForgetCredsException(Exception):
    pass

class KeyRingCredentials(AbstractCredentials):
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
