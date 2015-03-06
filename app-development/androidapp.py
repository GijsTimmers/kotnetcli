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

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

## We willen met meerdere schermen werken:
## - Startscherm: bevat de drie knoppen
## - Actiescherm: bevat de output, zoals bij --login en --logout. Kan evt.
##   gesplitst worden in een aparte Loginscherm en Logoutscherm.
## - Instellingenscherm: bevat meerdere widgets: "Gebruikersnaam", "Wachtwoord",
##   "Opslaan", "Vergeten", "Licenties". Het laatste veld kunnen we evt. ver-
##   vangen door een klein knopje op het hoofscherm.
## 
## Om dit allemaal proper aan elkaar te hangen, gebruiken we een ScreenManager:
## docs:        http://kivy.org/docs/api-kivy.uix.screenmanager.html
## uitlegvideo: https://www.youtube.com/watch?v=xx-NLOg6x8o



class Schermen():
    def __init__(self):
        
        ## Layout definiëren
        print "Laadt de Schermen-klasse in"
        
        self.b = BoxLayout(orientation="vertical")
        
        bnrtitle = Label(text="kotnetcli", font_size=30, size_hint_y=None, height=60)
        bnrsubtitle = Label(text="by Gijs Timmers and Jo Van Bulck", font_size=14, size_hint_y=None, height=30)
        
        kli = Button(text="Inloggen",     font_size=40, size_hint_y = 0.4)
        klo = Button(text="Uitloggen",    font_size=40, size_hint_y = 0.4)
        kls = Button(text="Instellingen", font_size=30, size_hint_y = 0.2)
        
        kli.bind(state=self.inlogscherm)
        
        self.b.add_widget(bnrtitle)
        self.b.add_widget(bnrsubtitle)
        self.b.add_widget(kli)
        self.b.add_widget(klo)
        self.b.add_widget(kls)
        
    

    def inlogscherm(self, instantie, waarde):
        ## Deze functie wordt aangeroepen door Schermen().kli
        if waarde == "down":
            print "KNOP=" + instantie.text
            print "Aangeklikt, moet nu gaan inloggen"
        
            self.b = BoxLayout(orientation="vertical")
            self.bnr = Label(text="Actiescherm", font_size=50)
            self.b.add_widget(self.bnr)
            
            return self.b

    def instellingenscherm(self):
        pass


class TutorialApp(App):
    def build(self):
        sch = Schermen()
        return sch.b

if __name__ == "__main__":
    TutorialApp().run()
