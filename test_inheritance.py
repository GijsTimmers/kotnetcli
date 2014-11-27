#!/usr/bin/env python2

import re                               ## Basislib voor reguliere expressies
import sys                              ## Basislib voor output en besturingssysteemintegratie
import time                             ## Voor timeout om venster te sluiten na login etc.
import curses                           ## Voor tekenen op scherm.
import keyring                          ## Voor ophalen wachtwoord
import getpass
import mechanize                        ## Emuleert een browser

class AbstractCommunicator( ):
            
    def kprint(self, pos_x, pos_y, tekst, attributes=None):
        raise NotImplementedError( "Should have implemented this" )

class VerboseCommunicator( AbstractCommunicator ):
    
    # nothing to initialize here
    
    def kprint(self, pos_x, pos_y, tekst, attributes=None):
        print tekst

class CursesCommunicator( AbstractCommunicator ):
    
    def __init__(self):
        self.scherm = curses.initscr()
        curses.curs_set(0)                  ## cursor invisible
        curses.start_color()                ## Kleuren aanmaken
        curses.use_default_colors()
        curses.init_pair(1, 1, -1)          ## Paren aanmaken: ndz vr curses.
        curses.init_pair(2, 2, -1)          ## Ik heb de curses-conventie aangehouden, 1 is dus rood,
        curses.init_pair(3, 3, -1)          ## 2 is groen, 3 is geel.
    
    def kprint(self, pos_x, pos_y, tekst, attributes):
        self.scherm.addstr(pos_x, pos_y, tekst, attributes)
        self.scherm.refresh()


## test code
co = VerboseCommunicator()
co.kprint(0,0, "hello world in plaintext")
time.sleep(2)

def testcurses(scherm):
    co = CursesCommunicator()
    co.kprint(0, 0, "hello world with curses\n", curses.color_pair(2) | curses.A_BOLD)
    time.sleep(2)

curses.wrapper(testcurses)
