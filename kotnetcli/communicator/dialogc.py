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
import quietc

class SuperDialogCommunicator(LoggerCommunicator):

    def __init__(self):
        self.d = Dialog()
        self.d.set_background_title("kotnetcli")
        
        self.WAIT     = "Wachten"
        self.DONE     = "In Orde"
        self.FAIL     = "Gefaald"
        self.CANCEL   = "Geskipt"
        self.NA       = "nvt"

        self.info     = ""
        self.overal   = 0
        ## we use a non-ordered dictionary here; event order is encapsulated in the
        ## login/logout subclasses via a custom self.iter iterator
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

    ## will be called by eventFailure methods inherited from QuietCommunicator
    def print_err(self, str):
        self.info = str
        ## fail the current item and cancel all following ones
        self.elements[self.iter.next()]      = self.FAIL
        for x in self.iter: self.elements[x] = self.CANCEL
        self.update()
    
    ################## COMMON LOGIN/LOGOUT COMMUNICATOR INTERFACE ##################
    
    def eventExit(self):
        ## print newline to clean prompt under dialog
        print("")
    
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

## end class SuperDialogCommunicator

class LoginDialogCommunicator(SuperDialogCommunicator):

    def __init__(self):
        super(LoginDialogCommunicator,self).__init__()

        self.title = "kotnetcli network login"
        self.elements["upload"]   = self.NA
        self.elements["download"] = self.NA
        
        ## create an iterator to keep track of the login progress
        self.iter = iter(["check", "get", "post", "process"])

    ################## APPEARANCE HELPER METHODS ##################

    def getProgressElements(self):
        return [ (quietc.STD_MSG_TEST,      self.elements["check"]),
                 (quietc.STD_MSG_GET,       self.elements["get"]),
                 (quietc.STD_MSG_POST,      self.elements["post"]),
                 (quietc.STD_MSG_PROCESS,   self.elements["process"]),                   
                 ("", ""),
                 ("Download",               self.elements["download"]),
                 ("Upload",                 self.elements["upload"])
               ]

    ################## LOGIN COMMUNICATOR INTERFACE ##################

    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.info = "Je bent successvol ingelogd."
        self.elements["process"]  = self.DONE
        self.elements["download"] = -downloadpercentage
        self.elements["upload"]   = -uploadpercentage
        self.overal = 100
        self.update()

## end class LoginDialogCommunicator
