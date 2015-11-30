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

