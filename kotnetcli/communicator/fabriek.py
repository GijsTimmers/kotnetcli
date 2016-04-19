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

## fabriek.py: zorgt op aanvraag van kotnetcli.py voor het aanmaken van de
## correcte communicator: bijvoorbeeld: kotnetcli.py vraagt om een login met
## curses als communicator; dan zal een instantie van 
## LoginCommunicatorFabriek.createCursesCommunicator() worden aangemaakt,
## genaamd co. Gezien LoginSummaryCommunicator() methodes bevat als 
## eventNetloginStart(), worden deze nu onderdeel van co. Dat wil zeggen dat
## de worker de juiste event kan aanroepen: bvb co.eventNetloginStart(), zonder
## te weten welke communicator dat nu precies is.
##
## LoginCommunicatorFabriek: functies als volgt aanroepen:
## co = LoginCommunicatorFabriek()       
## co = co.createColoramaCommunicator() 
## co.eventNetloginStart()               ## geeft de juiste output

class LoginCommunicatorFabriek():
    def createQuietCommunicator(self):
        from .quietc import QuietCommunicator
        return QuietCommunicator()
    
    def createPlaintextCommunicator(self):
        from .plaintextc import LoginPlaintextCommunicator
        return LoginPlaintextCommunicator()
    
    def createColoramaCommunicator(self):
        from .coloramac import LoginColoramaCommunicator
        return LoginColoramaCommunicator()


class LogoutCommunicatorFabriek():
    def createQuietCommunicator(self):
        raise Exception("logout not yet supported in beta")
    
    def createPlaintextCommunicator(self):
        raise Exception("logout not yet supported in beta")
    
    def createColoramaCommunicator(self):
        raise Exception("logout not yet supported in beta")
