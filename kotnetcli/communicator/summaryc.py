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

