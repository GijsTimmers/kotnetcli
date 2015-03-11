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

import re
import sys
import time                 ## Enkel om login te simuleren.

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock ## Om een interval in te bouwen, zonder de loop te blokkeren
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

class MenuScreen(Screen):
    pass

class ActionScreen(Screen):
    def inloggen(self):
        def update_tekst(*args):
            self.af_te_drukken_tekst = (
            "Netlogin openen...   [ OK ]", \
            "Netlogin openen...   [ OK ]\nGegevens invoeren... [ OK ]", \
            "Netlogin openen...   [ OK ]\nGegevens invoeren... [ OK ]\nGegevens opsturen... [ OK ]", \
            "Netlogin openen...   [ OK ]\nGegevens invoeren... [ OK ]\nGegevens opsturen... [ OK ]\nDownload:            [ 82%]\nUpload:              [100%]"
            )
            
            try:
                self.ids["outputvak"].text = self.af_te_drukken_tekst[self.index]
                self.index += 1
            except IndexError:
                ## indien index out of range (dus: einde bereikt): stop. Dat
                ## gaat volgens de documentatie door een False te returnen
                ## bij een methode die is aangeroepen door Clock.
                return False
            
            
        self.index = 0
        
        ## Gebruik Clock ipv time.sleep om tekst te updaten om de zoveel tijd
        Clock.schedule_interval(update_tekst, 0.5)

class SettingsScreen(Screen):
    pass


class TestApp(App):
    def build(self):
        ## Screen manager aanmaken
        
        self.menuscherm = MenuScreen(name="menu")
        self.actiescherm = ActionScreen(name="actie")
        self.instellingenscherm = SettingsScreen(name="settings")
        
        self.root = ScreenManager(transition=NoTransition())
        
        self.root.add_widget(self.menuscherm)
        self.root.add_widget(self.actiescherm)
        self.root.add_widget(self.instellingenscherm)
        
        return self.root
    
    def ga_naar_actiescherm_en_log_in(self):
        self.root.current = "actie"
        print self.root.current
        self.actiescherm.inloggen()
        
        

if __name__ == '__main__':
    TestApp().run()
