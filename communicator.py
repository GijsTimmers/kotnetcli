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
        self.tekstKleurRood = None
        self.tekstKleurGroen = None
        self.tekstKleurGeel = None
        self.tekstOpmaakVet = None
        self.tekstKleurGeelOpmaakVet = None

        self.tekstKleurRoodOpmaakVet = None
        self.tekstKleurGroenOpmaakVet = None
        self.tekstKleurGeelOpmaakVet = None
    
    def kprint(self, pos_y, pos_x, tekst, *args):
        pass
    
    def beeindig_sessie(self):
        pass

class PlaintextCommunicator(QuietCommunicator):
    def kprint(self, pos_y, pos_x, tekst, *args):
        if pos_y == 0:
            if tekst == "WAIT":
                print "Netlogin openen.......",
            if tekst == " OK ":
                print "OK"
        
        if pos_y == 1:
            if tekst == "WAIT":
                print "KU Leuven kiezen......",
            if tekst == " OK ":
                print "OK"
        
        if pos_y == 2:
            if tekst == "WAIT":
                print "Gegevens invoeren.....",
            if tekst == " OK ":
                print "OK"
                
        if pos_y == 3:
            if tekst == "WAIT":
                print "Gegevens opsturen.....",
            if tekst == " OK ":
                print "OK"
        
        if pos_y == 4:
            if re.compile(".[0-9]+.").match(tekst):
                print "Download: " + tekst.strip(" ")
        
        if pos_y == 5:
            if re.compile(".[0-9]+.").match(tekst):
                print "Upload: " + tekst.strip(" ")
        else:
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

    def kprint(self, pos_y, pos_x, tekst, *args):
        #print args
        if args:
            self.scherm.addstr(pos_y, pos_x, tekst, args[0])
            self.scherm.refresh()
        else:
            self.scherm.addstr(pos_y, pos_x, tekst)
            self.scherm.refresh()
    
    def beeindig_sessie(self):
        time.sleep(2)
        
        curses.nocbreak()
        self.scherm.keypad(0)
        curses.echo()
        curses.endwin()
        
