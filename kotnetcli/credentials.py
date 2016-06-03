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

class AbstractCredentials(object):

    def __init__(self, inst=None):
        self.inst = inst

    def getUser(self):
        return None
    
    def getPwd(self):
        return None
    
    def getInst(self):
        return self.inst
    
    def storeCreds(self, user, pwd, inst):
        self.inst = inst

    def hasCreds(self):
        return not (self.getUser() is None or
                    self.getPwd()  is None or
                    self.getInst() is None)
    
    def forgetCreds(self):
        self.inst = None

## end class AbstractCredentials

class GuestCredentials(AbstractCredentials):

    def __init__(self, inst=None):
        super(GuestCredentials, self).__init__(inst)
        self.user = None
        self.pwd = None
    
    def getUser(self):
        return self.user
    
    def getPwd(self):
        return self.pwd

    def storeCreds(self, user, pwd, inst):
        self.user = user
        self.pwd = pwd
        self.inst = inst
    
    def forgetCreds(self):
        self.user = None
        self.pwd = None
        self.inst = None

## end class GuestCredentials

class DummyCredentials(GuestCredentials):
    def __init__(self, inst=None):
        super(DummyCredentials, self).__init__(inst)
        self.user = "dummy_user"
        self.pwd  = "dummy_password"
        self.inst = inst

## end class DummyCredentials

class KeyRingCredentials(AbstractCredentials):
    def __init__(self, inst=None):
        super(KeyRingCredentials, self).__init__(inst)
        self.kr = keyring.get_keyring()

    def getUser(self):
        return self.kr.get_password("kotnetcli", "gebruikersnaam")
    
    def getPwd(self):
        return self.kr.get_password("kotnetcli", "wachtwoord")

    def getInst(self):
        krInst = self.kr.get_password("kotnetcli", "institution")
        return self.inst if self.inst is not None else krInst
    
    def storeCreds(self, user, pwd, inst):
        self.kr.set_password("kotnetcli", "wachtwoord", pwd)
        self.kr.set_password("kotnetcli", "gebruikersnaam", user)
        self.kr.set_password("kotnetcli", "institution", inst)
    
    def forgetCreds(self):
        try:
            self.kr.delete_password("kotnetcli", "gebruikersnaam")
            self.kr.delete_password("kotnetcli", "wachtwoord")
            self.kr.delete_password("kotnetcli", "institution")
        except keyring.errors.PasswordDeleteError:
            raise ForgetCredsException()

## end class KeyRingCredentials
