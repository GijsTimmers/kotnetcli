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

try:            
    print "Probeert Notify2 te importeren...",
    import notify2
    print "OK"
except ImportError:
    print "Couldn't import the notify2 library."
    pass


class SuperBubbleCommunicator(QuietCommunicator):
    def __init__(self):
        notify2.init("kotnetcli")

    def createAndShowNotification(title, message, icon):
        n = notify2.Notification(title, message, icon)
        n.show()

class LoginBubbleCommunicator(SuperBubbleCommunicator):
    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        createAndShowNotification( "Login geslaagd", "Download: %s%%, Upload: %s%%" % \
        (downloadpercentage, uploadpercentage), \
        "notification-network-ethernet-connected")
    
    def beeindig_sessie(self, error_code=0):
        if error_code == 0:
            pass
        else:
            createAndShowNotification( "Login mislukt", "Errorcode: %s" % \
            (error_code), "notification-network-ethernet-disconnected")   
        
class LogoutBubbleCommunicator(SuperBubbleCommunicator):
    def eventLogoutGeslaagd(self):
        n = notify2.Notification("Logout geslaagd", "", \
        "notification-network-ethernet-connected")
        n.show()
        
    def beeindig_sessie(self, error_code=0):
        if error_code == 0:
            pass
        else:
            createAndShowNotification( "Logout mislukt", "Errorcode: %s" % \
            (error_code), "notification-network-ethernet-connected")

