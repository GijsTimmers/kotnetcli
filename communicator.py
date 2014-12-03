#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten
import sys                              ## Basislib
import os                               ## Basislib

try:
    import curses                       ## Voor tekenen op scherm.
except ImportError:
    print "Windows-system detected. Will not import curses."

class QuietCommunicator():
    def __init__(self):
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
        
    def eventDownloadtegoedBekend(self, downloadpercentage):
        pass    
    def eventUploadtegoedBekend(self, uploadpercentage):
        pass
    
    def beeindig_sessie(self):
        pass

class PlaintextCommunicator(QuietCommunicator):
    def eventNetloginStart(self):
        print "Netlogin openen.......",
        sys.stdout.flush()
    def eventNetloginSuccess(self):
        print "[ OK ]"
    def eventNetloginFailure(self):
        print "[FAIL]"
        
    def eventKuleuvenStart(self):
        print "KU Leuven kiezen......",
        sys.stdout.flush()
    def eventKuleuvenSuccess(self):
        print "[ OK ]"
    def eventKuleuvenFailure(self):
        print "[FAIL]"

    def eventInvoerenStart(self):
        print "Gegevens invoeren.....",
        sys.stdout.flush()
    def eventInvoerenSuccess(self):
        print "[ OK ]"
    def eventInvoerenFailure(self):
        print "[FAIL]"

    def eventOpsturenStart(self):
        print "Gegevens opsturen.....",
        sys.stdout.flush()
    def eventOpsturenSuccess(self):
        print "[ OK ]"
    def eventOpsturenFailure(self):
        print "[FAIL]"
    
    def eventDownloadtegoedBekend(self, downloadpercentage):
        print "Download: " + " " * (3 - len(str(downloadpercentage))) + \
        str(downloadpercentage) + "%"
    
    def eventUploadtegoedBekend(self, uploadpercentage):
        print "Upload:   " + " " * (3 - len(str(uploadpercentage))) + \
        str(uploadpercentage) + "%"

class ColoramaCommunicator():
    pass

class SummaryCommunicator():
    pass

#class CursesCommunicator(QuietCommunicator):
class CursesCommunicator():
    def __init__(self):
        self.scherm = curses.initscr()
        
        curses.curs_set(0)                  ## cursor invisible
        curses.start_color()                ## Kleuren aanmaken
        curses.use_default_colors()
        curses.init_pair(1, 1, -1)          ## Paren aanmaken: ndz vr curses.
        curses.init_pair(2, 2, -1)          ## Ik heb de curses-conventie
        curses.init_pair(3, 3, -1)          ## aangehouden, 1 is dus rood,
                                            ## 2 is groen, 3 is geel.
        
        self.tekstKleurRood = curses.color_pair(1)
        self.tekstKleurGroen = curses.color_pair(2)
        self.tekstKleurGeel = curses.color_pair(3)
        self.tekstOpmaakVet = curses.A_BOLD
        
        self.tekstKleurRoodOpmaakVet = curses.color_pair(1) | curses.A_BOLD
        self.tekstKleurGroenOpmaakVet = curses.color_pair(2) | curses.A_BOLD
        self.tekstKleurGeelOpmaakVet = curses.color_pair(3) | curses.A_BOLD
        
        self.scherm.addstr(0, 0, "Netlogin openen.......")
        self.scherm.addstr(0, 22, "[    ]", self.tekstOpmaakVet)
        self.scherm.addstr(0, 23, "WAIT", self.tekstKleurGeelOpmaakVet)
        self.scherm.addstr(1, 0, "KU Leuven kiezen......")
        self.scherm.addstr(1, 22, "[    ]", self.tekstOpmaakVet)
        self.scherm.addstr(2, 0, "Gegevens invoeren.....")
        self.scherm.addstr(2, 22, "[    ]", self.tekstOpmaakVet)
        self.scherm.addstr(3, 0, "Gegevens opsturen.....")
        self.scherm.addstr(3, 22, "[    ]", self.tekstOpmaakVet)
        self.scherm.addstr(4, 0, "Download:")
        self.scherm.addstr(4, 10, "[          ][    ]", self.tekstOpmaakVet)
        self.scherm.addstr(5, 0, "Upload:")
        self.scherm.addstr(5, 10, "[          ][    ]", self.tekstOpmaakVet)
        
        self.scherm.refresh()
    
    def kprint(self, pos_y, pos_x, tekst, *args):
        if args:
            self.scherm.addstr(pos_y, pos_x, tekst, args[0])
            self.scherm.refresh()
        else:
            self.scherm.addstr(pos_y, pos_x, tekst)
            self.scherm.refresh()

    def eventNetloginStart(self):
        self.kprint(0, 23, "WAIT", self.tekstKleurGeelOpmaakVet)
    def eventNetloginSuccess(self):
        self.kprint(0, 23, " OK ", self.tekstKleurGroenOpmaakVet)
    def eventNetloginFailure(self):
        self.kprint(0, 23, "FAIL", self.tekstKleurRoodOpmaakVet)
        
    def eventKuleuvenStart(self):
        self.kprint(1, 23, "WAIT", self.tekstKleurGeelOpmaakVet)
    def eventKuleuvenSuccess(self):
        self.kprint(1, 23, " OK ", self.tekstKleurGroenOpmaakVet)
    def eventKuleuvenFailure(self):
        self.kprint(1, 23, "FAIL", self.tekstKleurRoodOpmaakVet)

    def eventInvoerenStart(self):
        self.kprint(2, 23, "WAIT", self.tekstKleurGeelOpmaakVet)
    def eventInvoerenSuccess(self):
        self.kprint(2, 23, " OK ", self.tekstKleurGroenOpmaakVet)
    def eventInvoerenFailure(self):
        self.kprint(2, 23, "FAIL", self.tekstKleurRoodOpmaakVet)

    def eventOpsturenStart(self):
        self.kprint(3, 23, "WAIT", self.tekstKleurGeelOpmaakVet)
    def eventOpsturenSuccess(self):
        self.kprint(3, 23, " OK ", self.tekstKleurGroenOpmaakVet)
    def eventOpsturenFailure(self):
        self.kprint(3, 23, "FAIL", self.tekstKleurRoodOpmaakVet)
    
    def eventDownloadtegoedBekend(self, downloadpercentage):
        balkgetal_download = int(round(float(downloadpercentage) / 10.0))
        
        if downloadpercentage <= 10:
            voorwaardelijke_kleur_download = \
            self.tekstKleurRoodOpmaakVet
        elif 10 < downloadpercentage < 60:
            voorwaardelijke_kleur_download = \
            self.tekstKleurGeelOpmaakVet
        else:
            voorwaardelijke_kleur_download = \
            self.tekstKleurGroenOpmaakVet
            
        self.kprint(4, 23, " " * (3 - len(str(downloadpercentage))) + \
        str(downloadpercentage) + \
        "%", voorwaardelijke_kleur_download)
        
        self.kprint(4, 11, "=" * balkgetal_download + \
        " " * (10-balkgetal_download), voorwaardelijke_kleur_download)
    
    def eventUploadtegoedBekend(self, uploadpercentage):
        balkgetal_upload = \
        int(round(float(uploadpercentage) / 10.0))
        
        if uploadpercentage <= 10:
            voorwaardelijke_kleur_upload = \
            self.tekstKleurRoodOpmaakVet
        elif 10 < uploadpercentage < 60:
            voorwaardelijke_kleur_upload = \
            self.tekstKleurGeelOpmaakVet
        else:
            voorwaardelijke_kleur_upload = \
            self.tekstKleurGroenOpmaakVet
        
        self.kprint(5, 23, " " * (3 - len(str(uploadpercentage))) + \
        str(uploadpercentage) + \
        "%", voorwaardelijke_kleur_upload)
    
        self.kprint(5, 11, "=" * balkgetal_upload + \
        " " * (10-balkgetal_upload), voorwaardelijke_kleur_upload)
        
    def beeindig_sessie(self):
        time.sleep(2)
        
        curses.nocbreak()
        self.scherm.keypad(0)
        curses.echo()
        curses.endwin()
        
