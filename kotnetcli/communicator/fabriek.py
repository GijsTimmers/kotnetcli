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

import atexit

inst_dict = { "kuleuven"           : "voor KU Leuven associatie",
              "kuleuven-campusnet" : "voor KU Leuven residenties",
              "kotnetext"          : "voor externen",
              "kuleuven-guest"     : "voor gasten"
            }

## co.eventExit is always called, even on asynchronous exit (e.g. keyboard interrupt)
## --> allow the communicator to restore user interface state (e.g. show cursor)
def wrap(coClass):
    co = coClass(inst_dict)
    atexit.register(co.eventExit)
    return co

class LoginCommunicatorFabriek(object):
    
    def createQuietCommunicator(self):
        from .quietc import QuietCommunicator
        return wrap(QuietCommunicator)
    
    def createLoggerCommunicator(self):
        from .loggerc import LoggerCommunicator
        return wrap(LoggerCommunicator)
    
    def createPlaintextCommunicator(self):
        from .plaintextc import LoginPlaintextCommunicator
        return wrap(LoginPlaintextCommunicator)
    
    def createColoramaCommunicator(self):
        from .coloramac import LoginColoramaCommunicator
        return wrap(LoginColoramaCommunicator)
    
    def createDialogCommunicator(self):
        from .dialogc import LoginDialogCommunicator
        return wrap(LoginDialogCommunicator)

    def createSummaryCommunicator(self):
        from .summaryc import LoginSummaryCommunicator
        return wrap(LoginSummaryCommunicator)

## end class LoginCommunicatorFabriek

class ForgetCommunicatorFabriek(LoginCommunicatorFabriek):
    
    def createPlaintextCommunicator(self):
        from .plaintextc import ForgetPlaintextCommunicator
        return wrap(ForgetPlaintextCommunicator)
    
    def createColoramaCommunicator(self):
        from .coloramac import ForgetColoramaCommunicator
        return wrap(ForgetColoramaCommunicator)

    def createDialogCommunicator(self):
        from .dialogc import ForgetDialogCommunicator
        return wrap(ForgetDialogCommunicator)

    def createSummaryCommunicator(self):
        from .summaryc import ForgetSummaryCommunicator
        return wrap(ForgetSummaryCommunicator)

## end class ForgetCommunicatorFabriek

class LogoutCommunicatorFabriek(object):
    
    def __init__(self):
        raise NotImplementedError
    
## end class LogoutCommunicatorFabriek
