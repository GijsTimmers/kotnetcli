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

## fabriek.py: zorgt op aanvraag van kotnetcli.py voor het aanmaken van de
## correcte communicator: bijvoorbeeld: kotnetcli.py vraagt om een login met
## curses als communicator; dan zal een instantie van 
## LoginCommunicatorFabriek.createCursesCommunicator() worden aangemaakt,
## genaamd co. Gezien LoginSummaryCommunicator() methodes bevat als 
## eventNetloginStart(), worden deze nu onderdeel van co. Dat wil zeggen dat
## de worker de juiste event kan aanroepen: bvb co.eventNetloginStart(), zonder
## te weten welke communicator dat nu precies is.

## Gijs@Jo: Dit was mijn interpretatie, is deze correct?

#from quietc     import LoginQuietCommunicator,     LogoutQuietCommunicator
#from summaryc   import LoginSummaryCommunicator,   LogoutSummaryCommunicator
#from bubblec    import LoginBubbleCommunicator,    LogoutBubbleCommunicator

#from cursesc    import LoginCursesCommunicator,    LogoutCursesCommunicator
#from dialogc    import DialogCommunicator
## Gijs@Jo: Graag aanpassen zodra de LoginDialogCommunicator en
##          LogoutDialogCommunicator af is.


## NOTE: lazy importing in the corresponding factory methods :-)

## The abstract factory specifying the interface and maybe returning 
## some defaults (or just passing)
class SuperCommunicatorFabriek:
    def createSummaryCommunicator():
        pass

## LoginCommunicatorFabriek: functies als volgt aanroepen:
## co = LoginCommunicatorFabriek()       
## co = co.createColoramaCommunicator() 
## co.eventNetloginStart()               ## geeft de juiste output

DEFAULT_COLORAMA_COLORS= [ "green", "yellow", "red", "bright" ]

class LoginCommunicatorFabriek(SuperCommunicatorFabriek):
    #def createQuietCommunicator(self):
    #    return LoginQuietCommunicator()
    
    def createPlaintextCommunicator(self):
        from plaintextc import LoginPlaintextCommunicator
        return LoginPlaintextCommunicator()
    
    def createColoramaCommunicator(self, colorNameList=DEFAULT_COLORAMA_COLORS):
        from coloramac import LoginColoramaCommunicator
        return LoginColoramaCommunicator(colorNameList)

    def createSummaryCommunicator(self):
        return LoginSummaryCommunicator()
    
    def createBubbleCommunicator(self):
        return LoginBubbleCommunicator()
    
    def createCursesCommunicator(self):
        return LoginCursesCommunicator()
    
    def createDialogCommunicator(self):
        return DialogCommunicator()
        ## Gijs@Jo: Ook hier graag aanpassen

class LogoutCommunicatorFabriek(SuperCommunicatorFabriek):
    def createSummaryCommunicator(self):
        return LogoutSummaryCommunicator()
     
    def createBubbleCommunicator(self):
        return LogoutBubbleCommunicator()
    
    def createPlaintextCommunicator(self):
        return LogoutPlaintextCommunicator()
    
    def createColoramaCommunicator(self):
        return LogoutColoramaCommunicator()
    
    def createCursesCommunicator(self):
        return LogoutCursesCommunicator()
    
    def createDialogCommunicator(self):
        return DialogCommunicator()
        ## Gijs@Jo: Ook hier graag aanpassen
