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

## pythondialog expects Python3-style unicode strings; for now the import below
## should work, but we want to remove this when switching to python3
## see also issue #84 and https://pypi.python.org/pypi/python2-pythondialog
from __future__ import unicode_literals

from dialog import Dialog
from loggerc import LoggerCommunicator

DIALOG_MSG_LOGIN_SUCCESS    = "Je bent successvol ingelogd."
DIALOG_MSG_FORGET_SUCCESS   = "You have succesfully removed your kotnetcli credentials."

class AbstractDialogCommunicator(LoggerCommunicator):

    def __init__(self, inst_dict):
        super(AbstractDialogCommunicator, self).__init__(inst_dict)
        self.d = Dialog()
        self.d.set_background_title("kotnetcli")

    def eventExit(self):
        ## print newline to clean prompt under dialog
        print("")

## end class AbstractDialogCommunicator

class ForgetDialogCommunicator(AbstractDialogCommunicator):
    
    def eventForgetCredsSuccess(self):
        self.d.msgbox(DIALOG_MSG_FORGET_SUCCESS)
   
    def eventFailureForget(self):
        self.d.msgbox(self.err_forget)
   
## end class ForgetDialogCommunicator

class SuperNetDialogCommunicator(AbstractDialogCommunicator):

    def __init__(self, inst_dict, title):
        super(SuperNetDialogCommunicator, self).__init__(inst_dict)
        
        self.WAIT     = "Wachten"
        self.DONE     = "In Orde"
        self.FAIL     = "Gefaald"
        self.CANCEL   = "Geskipt"
        self.NA       = "nvt"

        self.title    = title
        self.info     = ""
        self.overal   = 0
        ## we use a non-ordered dictionary here; event order is encapsulated in
        ## the login/logout subclasses via a custom self.iter iterator
        self.elements = { "check"   : self.WAIT,
                          "get"     : self.WAIT,
                          "post"    : self.WAIT,
                          "process" : self.WAIT
                        }
    
    ################## APPEARANCE HELPER METHODS ##################
    
    def update(self):
        self.d.mixedgauge(title    = self.title,
                          text     = self.info,
                          percent  = self.overal,
                          elements = self.getProgressElements())

    def eventError(self, string):
        self.info = string
        ## fail the current item and cancel all following ones
        self.elements[self.iter.next()]      = self.FAIL
        for x in self.iter: self.elements[x] = self.CANCEL
        self.update()
    
    ################## COMMON LOGIN/LOGOUT COMMUNICATOR INTERFACE ##############
    
    def eventPromptCredentials(self):
        instChoices = [(k, v, k=="kuleuven") for k,v in self.inst_dict.items()]
        (code, inst) = self.d.radiolist(text=self.inst_prompt, width=70,
                                                choices=instChoices)
        if code == Dialog.OK:
            (code, username) = self.d.inputbox(self.user_prompt,
                                                width=len(self.user_prompt)+6)
        if code == Dialog.OK:
            ## echo an asterisk for each character entered by the user
            (code, pwd) = self.d.passwordbox(self.pwd_prompt, insecure=True)
        if code != Dialog.OK:
            raise Exception
        return (username, pwd, inst)
    
    def eventCheckNetworkConnection(self):
        self.update()
    
    def eventGetData(self):
        self.elements[self.iter.next()] = self.DONE
        self.overal = 20
        self.update()
    
    def eventPostData(self):
        self.elements[self.iter.next()] = self.DONE
        self.overal = 50
        self.update()
    
    def eventProcessData(self):
        self.elements[self.iter.next()] = self.DONE
        self.overal = 80
        self.update()

## end class SuperNetworkCommunicator

class LoginDialogCommunicator(SuperNetDialogCommunicator):

    def __init__(self, inst_dict):
        super(LoginDialogCommunicator,self).__init__(inst_dict,
                                                    "kotnetcli network login")

        self.elements["upload"]   = self.NA
        self.elements["download"] = self.NA
        
        ## create an iterator to keep track of the login progress
        self.iter = iter(["check", "get", "post", "process"])

    ################## APPEARANCE HELPER METHODS ##################

    def getProgressElements(self):
        return [ (self.msg_test,    self.elements["check"]),
                 (self.msg_get,     self.elements["get"]),
                 (self.msg_post,    self.elements["post"]),
                 (self.msg_process, self.elements["process"]),
                 ("", ""),
                 ("Download",       self.elements["download"]),
                 ("Upload",         self.elements["upload"])
               ]

    ################## LOGIN COMMUNICATOR INTERFACE ##################

    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.info = DIALOG_MSG_LOGIN_SUCCESS
        self.elements["process"]  = self.DONE
        self.elements["download"] = -downloadpercentage
        self.elements["upload"]   = -uploadpercentage
        self.overal = 100
        self.update()

## end class LoginDialogCommunicator
