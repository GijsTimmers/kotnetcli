#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers
## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten na login etc.
import getpass                          ## Voor invoer wachtwoord zonder feedback
import curses                           ## Voor tekenen op scherm.
import sys                              ## Basislib voor output en besturingssysteemintegratie
import os                               ## Basislib voor besturingssysteemintegratie

class Communicator():
    ## ...let me do the talking...
    def __init__(self, verbosity):
        
        self.verbosity = verbosity
        
        if self.verbosity == "quiet":
            pass
        elif self.verbosity == "nocursing":
            pass
        elif self.verbosity == "cursing":
            #curses.wrapper(kprint)
            
            curses.initscr()
            curses.curs_set(0)                  ## cursor invisible
            curses.start_color()                ## Kleuren aanmaken
            curses.use_default_colors()
            curses.init_pair(1, 1, -1)          ## Paren aanmaken: ndz vr curses.
            curses.init_pair(2, 2, -1)          ## Ik heb de curses-conventie aangehouden, 1 is dus rood,
            curses.init_pair(3, 3, -1)          ## 2 is groen, 3 is geel.
            
    def kprint(self, pos_x, pos_y, tekst, attributes=None):
        if self.verbosity == "quiet":
            pass
        elif self.verbosity == "nocursing":
            pass
        elif self.verbosity == "cursing":
            self.scherm.addstr(pos_x, pos_y, tekst, attributes)
            self.scherm.refresh()
    
