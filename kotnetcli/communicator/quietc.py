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

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import sys                              ## Basislib
import os                               ## Basislib
import platform                         ## Om onderscheid Lin/Mac te maken
#from ..tools import cursor                ## Om cursor te verbergen/tonen
from tools import cursor                ## Om cursor te verbergen/tonen

## Gijs:
## We hoeven geen relatieve import te gebruiken omdat de map waarin 
## kotnetcli.py zich bevindt de rootmap ($PYTHONPATH) is. De map 'tools'
## bevindt zich daar ook; daarom hoeven we niet te verwijzen naar de lokatie
## ten opzichte van deze specifieke communicator (denk ik)


class QuietCommunicator():   
    def __init__(self):
        pass
    
    def eventPingSuccess(self):
        pass
    def eventPingFailure(self):
        pass
    def eventPingAlreadyOnline(self):
        pass

    def eventNetloginStart(self):
        pass
    def eventNetloginSuccess(self):
        pass
    def eventNetloginFailure(self):
        pass
        
    def eventKuleuvenStart(self):
        pass
    def eventKuleuvenSuccess(self):
        pass
    def eventKuleuvenFailure(self):
        pass

    def eventInvoerenStart(self):
        pass
    def eventInvoerenSuccess(self):
        pass
    def eventInvoerenFailure(self):
        pass

    def eventOpsturenStart(self):
        pass
    def eventOpsturenSuccess(self):
        pass
    def eventOpsturenFailure(self):
        pass
        
    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        pass
    def eventLogoutGeslaagd(self):
        pass
    
    ## TODO jo: moet 'error_code=0' hier niet vervangen worden door
    ## gewoon 'error_code'? en ook in de child classes??
    ## 
    ## Gijs: Voordeel hier is dat als er geen error code wordt meegegeven,
    ## de beeindig_sessie naar een error_code van 0 default. Dat betekent
    ## dat we gewoon beeindig_sessie() kunnen aanroepen als alles goed gaat.
    ## Vind ik duidelijker dan beeindig_sessie(0).
    ## Alternatief: steeds beeindig_sessie samen met het argument aanroepen:
    ## bvb beeindig_sessie(error_code=0), of beeindig_sessie(error_code=67)
    ## Hoe dan ook gaat mijn voorkeur uit naar één van deze methodes in plaats
    ## van het toch wat vreemde beeindig_sessie(0).
    
    def beeindig_sessie(self, error_code=0):
        pass
