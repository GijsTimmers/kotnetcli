#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

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

from colorama import (                  ## Om de tekst kleur te geven
    Fore,                               ## 
    Style,                              ## 
    init as colorama_init)              ## 
    
if os.name == "posix":
    try:            
        import curses                       ## Voor tekenen op scherm.
    except ImportError:
        print "Couldn't import the curses library."
        pass
    try:            
        import notify2                      ## OS-specifieke notificaties
    except ImportError:
        print "Couldn't import the notify2 library."
        pass
    try:            
        from dialog import Dialog           ## Voor tekenen op scherm.
    except ImportError:
        print "Couldn't import the dialog library."
        pass
if os.name == "nt":
    print "Windows system detected. Will not import curses, notify and dialog"

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
        
    def eventTegoedenBekend(self, downloadpercentage, uploadpercentage):
        pass
    
    def beeindig_sessie(self, error_code=0):
        pass

class BubbleCommunicator(QuietCommunicator):
    def __init__(self):
        notify2.init("kotnetcli")
    def eventTegoedenBekend(self, downloadpercentage, uploadpercentage):
        n = notify2.Notification("kotnetcli", \
        "Download: %s%%, Upload: %s%%" % \
        (downloadpercentage, uploadpercentage), \
        "notification-network-ethernet-connected")
        n.show()

class DialogCommunicator(QuietCommunicator):
    def __init__(self):
        
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
    
    def eventTegoedenBekend(self, downloadpercentage, uploadpercentage):
        self.download = -downloadpercentage
        self.upload = -uploadpercentage
        self.overal = 100
        self.update()
        
    def beeindig_sessie(self, error_code=0):
        print "" # print newline to clean prompt under dialog

class SummaryCommunicator(QuietCommunicator):
    def eventPingFailure(self):
        print "Niet verbonden met het KU Leuven-netwerk."
    def eventPingAlreadyOnline(self):
        print "U bent al online."
    
    def eventTegoedenBekend(self, downloadpercentage, uploadpercentage):
        print "Download: " + str(downloadpercentage) + "%" + ",",
        print "Upload: " + str(uploadpercentage) + "%"        

class ColoramaCommunicator(QuietCommunicator):
    def __init__(self):
        colorama_init()
        if os.name == "posix":
            ## Hide the terminal cursor using ANSI escape codes
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
    
    def eventPingFailure(self):
        print Style.BRIGHT + Fore.RED + \
        "Niet verbonden met het KU Leuven-netwerk." + \
        Style.RESET_ALL + Fore.RESET
    def eventPingAlreadyOnline(self):
        print Style.BRIGHT + Fore.YELLOW + \
        "U bent al online." + \
        Fore.RESET + Style.RESET_ALL
    
    def eventNetloginStart(self):
        print "Netlogin openen....... " + Style.BRIGHT + "[" + Fore.YELLOW + \
        "WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        sys.stdout.flush()
    def eventNetloginSuccess(self):
        print Style.BRIGHT + "[" + Fore.GREEN + " OK " + \
        Fore.RESET + "]" + Style.RESET_ALL
    def eventNetloginFailure(self):
        print Style.BRIGHT + "[" + Fore.RED + "FAIL" + \
        Fore.RESET + "]" + Style.RESET_ALL
        
    def eventKuleuvenStart(self):
        print "KU Leuven kiezen...... " + Style.BRIGHT + "[" + Fore.YELLOW + \
        "WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        sys.stdout.flush()
    def eventKuleuvenSuccess(self):
        print Style.BRIGHT + "[" + Fore.GREEN + " OK " + \
        Fore.RESET + "]" + Style.RESET_ALL
    def eventKuleuvenFailure(self):
        print Style.BRIGHT + "[" + Fore.RED + "FAIL" + \
        Fore.RESET + "]" + Style.RESET_ALL

    def eventInvoerenStart(self):
        print "Gegevens invoeren..... " + Style.BRIGHT + "[" + Fore.YELLOW + \
        "WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        sys.stdout.flush()
    def eventInvoerenSuccess(self):
        print Style.BRIGHT + "[" + Fore.GREEN + " OK " + \
        Fore.RESET + "]" + Style.RESET_ALL
    def eventInvoerenFailure(self):
        print Style.BRIGHT + "[" + Fore.RED + "FAIL" + \
        Fore.RESET + "]" + Style.RESET_ALL

    def eventOpsturenStart(self):
        print "Gegevens opsturen..... " + Style.BRIGHT + "[" + Fore.YELLOW + \
        "WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        sys.stdout.flush()
    def eventOpsturenSuccess(self):
        print Style.BRIGHT + "[" + Fore.GREEN + " OK " + \
        Fore.RESET + "]" + Style.RESET_ALL
    def eventOpsturenFailure(self):
        print Style.BRIGHT + "[" + Fore.RED + "FAIL" + \
        Fore.RESET + "]" + Style.RESET_ALL
    
    def eventTegoedenBekend(self, downloadpercentage, uploadpercentage):
        print "Download:  " + Style.BRIGHT + "[          ][    ]" + \
        Style.RESET_ALL + "\r",
        
        balkgetal_download = int(round(float(downloadpercentage) / 10.0))
        
        if downloadpercentage <= 10:
            voorwaardelijke_kleur_download = \
            Fore.RED
        elif 10 < downloadpercentage < 60:
            voorwaardelijke_kleur_download = \
            Fore.YELLOW
        else:
            voorwaardelijke_kleur_download = \
            Fore.GREEN
        
        print "Download:  " + \
        Style.BRIGHT + "[" + voorwaardelijke_kleur_download + \
        "=" * balkgetal_download + Fore.RESET + \
        " " * (10-balkgetal_download) + \
        "]" + \
        "[" + \
        " " * (3 - len(str(downloadpercentage))) + \
        voorwaardelijke_kleur_download + str(downloadpercentage) + \
        "%" + Fore.RESET + \
        "]" + Style.RESET_ALL
        
        print "Upload:    " + Style.BRIGHT + "[          ][    ]" + \
        Style.RESET_ALL + "\r",
        
        balkgetal_upload = int(round(float(uploadpercentage) / 10.0))
            
        if uploadpercentage <= 10:
            voorwaardelijke_kleur_upload = \
            Fore.RED
        elif 10 < uploadpercentage < 60:
            voorwaardelijke_kleur_upload = \
            Fore.YELLOW
        else:
            voorwaardelijke_kleur_upload = \
            Fore.GREEN
        
        print "Upload:    " +  \
        Style.BRIGHT + "[" + voorwaardelijke_kleur_upload + \
        "=" * balkgetal_upload + Fore.RESET + \
        " " * (10-balkgetal_upload) + \
        "]" + \
        "[" + \
        " " * (3 - len(str(uploadpercentage))) + \
        voorwaardelijke_kleur_upload + str(uploadpercentage) + \
        "%" + Fore.RESET + \
        "]" + Style.RESET_ALL
    
    def beeindig_sessie(self, error_code=0):
        if os.name == "posix":
            ## re-display the terminal cursor using ANSI escape codes
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
        else:
            time.sleep(3)            


class PlaintextCommunicator(ColoramaCommunicator):
    def __init__(self):
        Style.BRIGHT = ""
        Style.RESET = ""
        Fore.GREEN = ""
        Fore.YELLOW = ""
        Fore.RED = ""

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
    
    def eventPingSuccess(self):
        pass
    
    def eventPingFailure(self):
        self.kprint(6, 0, "Niet verbonden met het KU Leuven-netwerk.", \
        self.tekstKleurRoodOpmaakVet)
    def eventPingAlreadyOnline(self):
        self.kprint(6, 0, "U bent al online.", \
        self.tekstKleurGeelOpmaakVet)
        
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
    
    def eventTegoedenBekend(self, downloadpercentage, uploadpercentage):
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
        
    def beeindig_sessie(self, error_code=0):
        time.sleep(2)
        
        curses.nocbreak()
        self.scherm.keypad(0)
        curses.echo()
        curses.endwin()
        
