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

from quietc     import QuietCommunicator
from summaryc   import LoginSummaryCommunicator,   LogoutSummaryCommunicator
from bubblec    import LoginBubbleCommunicator,    LogoutBubbleCommunicator

from plaintextc import LoginPlaintextCommunicator, LogoutPlaintextCommunicator
from coloramac  import LoginColoramaCommunicator,  LogoutColoramaCommunicator

from cursesc    import LoginCursesCommunicator,    LogoutCursesCommunicator
from dialogc    import DialogCommunicator
## Gijs@Jo: Graag aanpassen zodra de LoginDialogCommunicator en
##          LogoutDialogCommunicator af is.


## The abstract factory specifying the interface and maybe returning 
## some defaults (or just passing)
class SuperCommunicatorFabriek:
    def createSummaryCommunicator():
        pass

class LoginCommunicatorFabriek(SuperCommunicatorFabriek):
    def createSummaryCommunicator():
        LoginSummaryCommunicator()
    
    def createBubbleCommunicator():
        LoginBubbleCommunicator()
    
    def createPlaintextCommunicator():
        LoginPlaintextCommunicator()
    
    def createColoramaCommunicator():
        LoginColoramaCommunicator()
    
    def createCursesCommunicator():
        LoginCursesCommunicator()
    
    def createDialogCommunicator():
        DialogCommunicator()
        ## Gijs@Jo: Ook hier graag aanpassen

class LogoutCommunicatorFabriek(SuperCommunicatorFabriek):
    def createSummaryCommunicator():
        LogoutSummaryCommunicator()
     
    def createBubbleCommunicator():
        LogoutBubbleCommunicator()
    
    def createPlaintextCommunicator():
        LogoutPlaintextCommunicator()
    
    def createColoramaCommunicator():
        LogoutColoramaCommunicator()
    
    def createCursesCommunicator():
        LogoutCursesCommunicator()
    
    def createDialogCommunicator():
        DialogCommunicator()
        ## Gijs@Jo: Ook hier graag aanpassen
