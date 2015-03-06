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


from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        id: hoofdbox
        orientation: "vertical"
        
        BoxLayout:
            id: titelbox
            orientation: "vertical"
            size_hint_y: 0.15
            
            
            Label:
                text: "kotnetcli"
                font_size: 30
                size_hint_y: 0.6
        
            Label:
                text: "by Gijs Timmers and Jo Van Bulck"
                font_size: 14
                size_hint_y: 0.4
            
        BoxLayout:
            id: knoppenbox
            orientation: "vertical"
            
            Button:
                id: inlogknop
                text: "Inloggen"
                on_press:
                    #root.manager.current = "action"
                    root.inloggen()
                
            Button:
                id: uitlogknop
                text: "Uitloggen"
                on_press:
                    root.manager.current = "action"
                    root.uitloggen()
            
            Button:
                id: instellingenknop
                text: "Instellingen"
                on_press: root.manager.current = "settings"


            Label:
                id: outputvak
                text: "Netlogin openen...   [ OK ]\\nGegevens invoeren... [ OK ]\\nGegevens opsturen... [ OK ]"
                font_size: 20
                font_name: "DroidSansMono.ttf"
            
            Button:
                id: terugknop
                text: "Terug naar hoofdmenu"
                #on_press: root.manager.current = "menu"
                on_press: root.herteken_hoofdmenu()
            
            Button:
                id: afsluitknop
                text: "Afsluiten"
                on_press: root.afsluiten()
            
        
<SettingsScreen>:
    BoxLayout:
        orientation: "vertical"
        
        Label:
            text: "kotnetcli"
            font_size: 30
            size_hint_y: None
            height: 60
        
        Label:
            text: "by Gijs Timmers and Jo Van Bulck"
            font_size: 14
            size_hint_y: None
            height: 30
        
        TextInput:
            id: veld_gebruikersnaam
            hint_text: "Gebruikersnaam"
            multiline: False
            size_hint_y: None
            height: 30
            keyboard_suggestions: False
            password: False
            write_tab: False
            #on_text_validate: root.stelGebruikersnaamIn(self.text)
        
        TextInput:
            id: veld_wachtwoord
            hint_text: "Wachtwoord"
            multiline: False
            size_hint_y: None
            height: 30
            keyboard_suggestions: False
            password: True
            write_tab: False
            #on_text_validate: root.stelWachtwoordIn(self.text)
        
        
        Button:
            text: "Opslaan"
            size_hint_y: 0.3
            on_press: root.toonData()
        
        Label:
            id: toonvak
            text: "Nog geen data ontvangen..."
        
        Button:
            text: "Terug naar hoofdmenu"
            size_hint_y: 0.2
            on_press: root.manager.current = 'menu'
            
""")



class MenuScreen(Screen):        
    def inloggen(self):
        print "Wens tot inloggen ontvangen."
        
        print self.ids
        
        self.ids["knoppenbox"].remove_widget(self.ids["inlogknop"])
        self.ids["knoppenbox"].remove_widget(self.ids["uitlogknop"])
        self.ids["knoppenbox"].remove_widget(self.ids["instellingenknop"])
        
    
    def uitloggen(self):
        print "Wens tot uitloggen ontvangen."
    
    def herteken_hoofdmenu(self):
        self.ids["knoppenbox"].add_widget(self.ids["inlogknop"])
        self.ids["knoppenbox"].add_widget(self.ids["uitlogknop"])
        self.ids["knoppenbox"].add_widget(self.ids["instellingenknop"])
        
        
        self.ids["knoppenbox"].remove_widget(self.ids["outputvak"])
        self.ids["knoppenbox"].remove_widget(self.ids["terugknop"])
        self.ids["knoppenbox"].remove_widget(self.ids["afsluitknop"])
    

class ActionScreen(Screen):
    def inloggen(self):
        print "Inloggen op actiescherm."
    def afsluiten(self):
        print "Sluit nu af."
        sys.exit()

class SettingsScreen(Screen):
    def toonData(self):
        self.gebruikersnaam = self.ids["veld_gebruikersnaam"].text
        self.wachtwoord     = self.ids["veld_wachtwoord"].text
        
        print "Nu ingevoerd:   "
        print "----------------"
        print "Gebruikersnaam: " + self.gebruikersnaam
        print "Wachtwoord:     " + self.wachtwoord
        print "----------------"
        
        ## Als de gebruikersnaam geen geldig s-/r-nummer is, of het wachtwoord
        ## is leeg, dan melden we dat.
        if (not re.match("[a-z][0-9]+", self.gebruikersnaam)) or (self.wachtwoord == ""):
            print "--> Check gegevens"
            self.ids["toonvak"].text = "Controleer uw gegevens."
        else:
            keyring = JsonStore("keyring.json")
            keyring.put("kotnetcli", \
                         gebruikersnaam = self.gebruikersnaam, \
                         wachtwoord     = self.wachtwoord)
            
            #print "gebruikersnaam in keyring: ", keyring.get("kotnetcli")["gebruikersnaam"]
            #print "wachtwoord in keyring: ", keyring.get("kotnetcli")["wachtwoord"]
            print "--> Opgeslagen"
            self.ids["toonvak"].text = "Opgeslagen."
            


# Create the screen manager
sm = ScreenManager(transition=NoTransition())
sm.add_widget(MenuScreen(name="menu"))
#sm.add_widget(ActionScreen(name="action"))
sm.add_widget(SettingsScreen(name="settings"))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
