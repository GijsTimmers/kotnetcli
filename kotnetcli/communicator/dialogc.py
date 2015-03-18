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
from quietc import QuietCommunicator
#from ..tools import cursor              ## Om cursor te verbergen/tonen
from tools import cursor                ## Om cursor te verbergen/tonen

## Gijs:
## We hoeven geen relatieve import te gebruiken omdat de map waarin 
## kotnetcli.py zich bevindt de rootmap ($PYTHONPATH) is. De map 'tools'
## bevindt zich daar ook; daarom hoeven we niet te verwijzen naar de lokatie
## ten opzichte van deze specifieke communicator (denk ik)


try:
    print "Probeert Dialog te importeren...",
    from dialog import Dialog           ## Voor tekenen op scherm.
    print "OK"
except ImportError:
    print "Couldn't import the dialog library."
    pass


## TODO jo: ik zal deze communicator nog opslitsen in een
## super en 2 subklassen als ik tijd heb...
class DialogCommunicator(QuietCommunicator):
    def __init__(self, uit_te_voeren_procedure):
        
        # some constant definitions to avoid using magic numbers
        # for the DialogCommunicator mixedgauge dialog
        self.WAIT        = 7
        self.DONE        = 0
        self.FAIL        = 1
        
        self.d = Dialog(dialog="dialog")
        self.d.set_background_title("kotnetcli")
        self.netlogin = self.WAIT
        self.kuleuven = self.WAIT
        self.invoeren = self.WAIT
        self.opsturen = self.WAIT
        self.download = self.WAIT
        self.upload = self.WAIT
        self.overal = 0
        self.update()
    
    def update(self):
        self.d.mixedgauge("",
            title="kotnetcli",
            percent= self.overal,
            elements= [ ("Netlogin openen", self.netlogin),
                        ("KU Leuven kiezen", self.kuleuven),
                        ("Gegevens invoeren", self.invoeren),
                        ("Gegevens opsturen", self.opsturen),                                   
                        ("", ""),
                        ("Download", self.download),
                        ("Upload", self.upload)
                      ])
    
    def eventPingFailure(self):
        self.d.infobox("Niet verbonden met het KU Leuven-netwerk.", 5, 30)
    def eventPingAlreadyOnline(self):
        self.d.infobox("U bent al online.", 5, 30)
    
    def eventNetloginSuccess(self):
        self.netlogin = self.DONE
        self.overal = 40
        self.update()
    def eventNetloginFailure(self):
        self.netlogin = self.FAIL
        self.overal = 40
        self.update()
    
    def eventKuleuvenSuccess(self):
        self.kuleuven = self.DONE
        self.overal = 60        
        self.update()
    def eventKuleuvenFailure(self):
        self.kuleuven = self.FAIL
        self.overal = 60        
        self.update()
    
    def eventInvoerenSuccess(self):
        self.invoeren = self.DONE
        self.overal = 80
        self.update()
    def eventInvoerenFailure(self):
        self.invoeren = self.FAIL
        self.overal = 80        
        self.update()

    def eventOpsturenSuccess(self):
        self.opsturen = self.DONE 
        self.overal = 100        
        self.update()
    def eventOpsturenFailure(self):
        self.opsturen = self.FAIL
        self.overal = 100        
        self.update()
    
    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        self.download = -downloadpercentage
        self.upload = -uploadpercentage
        self.overal = 100
        self.update()
        
    def beeindig_sessie(self, uitgevoerde_procedure=None, error_code=0):
        print "" # print newline to clean prompt under dialog


