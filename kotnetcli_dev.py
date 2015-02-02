#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To  view a copy of
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View,
## CA 94042, USA.

## kotnetcli_dev.py: an extension of kotnetcli.py, containing some
## extra developer/debug related command line options

from kotnetcli import KotnetCLI

class KotnetCLIDev(KotnetCLI):

    def voegArgumentenToe(self):
        super(KotnetCLIDev, self).voegArgumentenToe()
        
        self.workergroep.add_argument("-1", "--dummy-login",\
        help="Performs a dry-run logging in",\
        action="store_const", dest="worker", const="dummy_login")
        
        self.workergroep.add_argument("-0", "--dummy-logout",\
        help="Performs a dry-run logging out",\
        action="store_const", dest="worker", const="dummy_logout")
    
    def parseArgumenten(self):
        argumenten = self.parser.parse_args()
        cr = Credentials()
        
        if argumenten.worker == "dummy_login":
            print "ik wil inloggen voor spek en bonen"
            print "ik wil credentials ophalen voor spek en bonen"
            #creds = 
            #worker fabriek
            #co = self.parseCommunicatorFlags(fabriek)
            #worker.go(co, creds)

        
        elif argumenten.worker == "dummy_logout":
            print "ik wil uitloggen voor spek en bonen"
            print "ik wil credentials ophalen voor spek en bonen"
            #creds = 
            #worker fabriek
            #co = self.parseCommunicatorFlags(fabriek)            
            #worker.go(co, creds)

        else
            super(KotnetCLIDev, self).parseArgumenten()


## Start de zaak asa deze file rechtstreeks aangeroepen is vanuit
## command line (i.e. niet is geimporteerd vanuit een andere file)
if  __name__ =='__main__':
    print "== kotnetcli_dev started =="
    k = KotnetCLIDev()
    k.parseArgumenten()
    print "== kotnetcli_dev done =="
