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

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout



def scherm():
    
    b = BoxLayout(orientation="vertical")
        
    bnrtitle = Label(text="kotnetcli", font_size=30, size_hint_y=None, height=60)
    bnrsubtitle = Label(text="by Gijs Timmers and Jo Van Bulck", font_size=14, size_hint_y=None, height=30)
    
    ## Kopieer: cp /usr/share/fonts/truetype/droid/DroidSansMono.ttf .
    outputtekst =  Label(text="Netlogin openen...   [ OK ]\n" + \
                              "Gegevens invoeren... [ OK ]\n" + \
                              "Gegevens opsturen... [ OK ]",
                         font_size=20, font_name="DroidSansMono.ttf")
    
    b.add_widget(bnrtitle)
    b.add_widget(bnrsubtitle)
    b.add_widget(outputtekst)
    
    return b
    
    
    


class TutorialApp(App):
    def build(self):
        return scherm()

if __name__ == "__main__":
    TutorialApp().run()
