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

from quietc import QuietCommunicator
        
## Abstract super class (not intended to directly create), encapsulating 
## things common to a Login- and LogoutSummaryCommunicator
class SuperSummaryCommunicator(QuietCommunicator):
    def eventPingFailure(self):
        print "Niet verbonden met het KU Leuven-netwerk."
    def eventPingAlreadyOnline(self):
        print "U bent al online."

class LoginSummaryCommunicator(SuperSummaryCommunicator):
    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        print "Login geslaagd."
        print "Download: " + str(downloadpercentage) + "%" + ",",
        print "Upload: " + str(uploadpercentage) + "%"

    def beeindig_sessie(self, error_code=0):
        if error_code == 0:
            pass
        else:
            print "Login mislukt."

class LogoutSummaryCommunicator(SuperSummaryCommunicator):
    def eventLogoutGeslaagd(self):
        print "Logout geslaagd."
        
    def beeindig_sessie(self, error_code=0):
        if error_code == 0:
            pass
        else:
            print "Logout mislukt."

