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
import threading
import mechanize
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock ## Om een interval in te bouwen, zonder de loop te blokkeren
from kivy.storage.jsonstore import JsonStore

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from pygments.lexers import TextLexer

class MenuScreen(Screen):
    pass

class ActionScreen(Screen):
    def print_generic_balk(self, percentage, style, color, stop_color, stop_style):        
            percentagefloat = float(percentage)
            percentagestring = str(percentage)
            
            lengteVanBalkfloat = 15.0
            lengteVanBalkint = 15
            lengteVanRuimteVoorPercentages = 3
            
            aantalStreepjesObvPercentage = int(round(percentagefloat/100.0 * lengteVanBalkfloat))
            return style + "[" + color + \
            "=" * aantalStreepjesObvPercentage + stop_color + \
            " " * (lengteVanBalkint-aantalStreepjesObvPercentage) + \
            "][" + \
            " " * (lengteVanRuimteVoorPercentages - len(percentagestring)) + \
            color + percentagestring + "%" + \
            stop_color + "]" + stop_style
        
    def print_balk(self, percentage):
            return self.print_generic_balk(percentage, "", "", "", "")
    

    def inloggen(self):
        self.ids["outputvak"].text = "Netlogin openen.......... "
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        response = self.browser.open("https://netlogin.kuleuven.be/cgi-bin/wayf2.pl?inst=kuleuven&lang=nl&submit=Ga+verder+%2F+Continue", \
        timeout=1.5)
        self.ids["outputvak"].text += "[ OK ]\n"
        self.ids["voortgangsbalk"].value = 33
        
        #self.ids["outputvak"].text = "Netlogin openen.......... [ OK ]\n"
        
        self.ids["outputvak"].text += "Gegevens invoeren........ "
        keyring = JsonStore("keyring.json")
        gebruikersnaam = keyring.get("kotnetcli")["gebruikersnaam"]
        wachtwoord     = keyring.get("kotnetcli")["wachtwoord"]
        
        print "----------------"
        print "Gebruikersnaam: " + gebruikersnaam
        print "Wachtwoord:     " + wachtwoord
        print "----------------"
        print "--> Opgehaald."
        
        
        self.browser.select_form(nr=1)
        self.browser.form["uid"] = gebruikersnaam
        wachtwoordvaknaam = \
        self.browser.form.find_control(type="password").name
        self.browser.form[wachtwoordvaknaam] = wachtwoord
        self.ids["outputvak"].text += "[ OK ]\n"
        self.ids["voortgangsbalk"].value = 66
        
        self.ids["outputvak"].text += "Gegevens opsturen........ "
        self.browser.submit()
        #self.ids["outputvak"].text += "Gegevens opsturen........ [ OK ]\n"
        
        
        html = unicode(self.browser.response().read(), "utf-8")
        #print html
        print "---------------------------------------------"
        print "---------------------------------------------"
        print "---------------------------------------------"
        
        ## Parsen gaat wél op PC, niet op Android: bs4 conflicteert met mechanize
        ## rond een bepaalde library, die ze allebei nodig hebben.
        ## Workaround: parsen met re ipv bs4.
        
        downstring       = re.findall("(?<=available download = )\d+ of \d+", html)[0]
        downverbruikt    = float(re.findall("\d+", downstring)[0])
        downtotaal       = float(re.findall("\d+", downstring)[1])
        downpercentage   = int(round(downverbruikt/downtotaal * 100))
        
        upstring         = re.findall("(?<=available upload = )\d+ of \d+", html)[0]
        upverbruikt      = float(re.findall("\d+", upstring)[0])
        uptotaal         = float(re.findall("\d+", upstring)[1])
        uppercentage     = int(round(upverbruikt/uptotaal * 100))
        
        print downpercentage
        print uppercentage
        
        self.ids["outputvak"].text += "[ OK ]\n"
        self.ids["outputvak"].text += "Download " + self.print_balk(downpercentage) + "\n"
        self.ids["outputvak"].text += "Upload   " + self.print_balk(uppercentage)   + "\n"
        self.ids["voortgangsbalk"].value = 100
        
        ## Thread eindigt vanzelf, want er is niks meer te doen.

        
    def uitloggen(self):
        ## Moet nog aan gewerkt worden.
        print "Ik wil uitloggen."
        self.ids["outputvak"].text += "Wordt aan gewerkt...\n"

class SettingsScreen(Screen):
    def saveOrForget(self):
        ## Bepaalt adhv de toestand van de opslaanvergeetknop of er opgeslagen
        ## dan wel vergeten moet worden.
        if self.ids["opslaanvergeetknop"].toestand == "opslaan":
            self.saveCredentials()
        elif self.ids["opslaanvergeetknop"].toestand == "vergeten":
            self.forgetCredentials()
    
    def saveCredentials(self):
        ## Leest de gegevens uit uit de velden. Indien er een foute gebruikers-
        ## naam is (bvb 0123456), of een leeg wachtwoord, krijgt de gebruiker
        ## een melding door verandering van de tekst op de knop. Indien het
        ## wel lijkt te kloppen, worden de gegevens opgeslagen in keyring.json.
        
        gebruikersnaam = self.ids["veld_gebruikersnaam"].text
        wachtwoord     = self.ids["veld_wachtwoord"].text
        
        print "----------------"
        print "Gebruikersnaam: " + gebruikersnaam
        print "Wachtwoord:     " + wachtwoord
        print "----------------"
        
        if (not re.match("[a-z][0-9]+", gebruikersnaam)) or (wachtwoord == ""):
            ## Als de gebruikersnaam geen geldig s-/r-nummer is, of het wachtwoord
            ## is leeg, dan wordt er niets opgeslagen en geven we een melding
            ## via de knop.
            print "--> Gegevens kloppen niet, controleer."
            self.ids["opslaanvergeetknop"].text = "Controleer uw gegevens en klik opnieuw."
        else:
            ## Als alles klopt, slaan we het op in de keyring.
            keyring = JsonStore("keyring.json")
            keyring.put("kotnetcli", \
                        gebruikersnaam = gebruikersnaam, \
                        wachtwoord     = wachtwoord)
            print "--> Opgeslagen in keyring.json."
            
            self.ids["opslaanvergeetknop"].toestand = "vergeten"
            self.ids["opslaanvergeetknop"].text = "Gebruikersnaam en wachtwoord opnieuw instellen"
            self.ids["opslaanvergeetknop"].background_color = [2.5, 1, 1, 1]
            self.ids["veld_gebruikersnaam"].disabled = True
            self.ids["veld_wachtwoord"].disabled = True
            self.ids["veld_gebruikersnaam"].text = gebruikersnaam
            self.ids["veld_wachtwoord"].text = wachtwoord
            self.ids["veld_gebruikersnaam"].font_size = 90
            
    
    def forgetCredentials(self):
        keyring = JsonStore("keyring.json")
        keyring.delete("kotnetcli")
        print "----------------"
        print "Gebruikersnaam: " + "????????"
        print "Wachtwoord:     " + "????????"
        print "----------------"
        print "--> Verwijderd uit keyring.json."
        self.ids["opslaanvergeetknop"].toestand = "opslaan"
        self.ids["opslaanvergeetknop"].text = "Opslaan"
        self.ids["opslaanvergeetknop"].background_color = [1, 1, 1, 1]
        self.ids["veld_gebruikersnaam"].disabled = False
        self.ids["veld_wachtwoord"].disabled = False
        self.ids["veld_gebruikersnaam"].text = ""
        self.ids["veld_wachtwoord"].text = ""
        self.ids["veld_gebruikersnaam"].font_size = 90


class KotnetApp(App):
    
    def build(self):
        ## Kivy-instellingen uitschakelen bij druk op Menu-knop
        self.use_kivy_settings = False        
        
        ## Screen manager aanmaken
        self.menuscherm = MenuScreen(name="menu")
        self.actiescherm = ActionScreen(name="actie")
        self.instellingenscherm = SettingsScreen(name="settings")
        
        self.root = ScreenManager(transition=NoTransition())
        self.root.add_widget(self.menuscherm)
        self.root.add_widget(self.actiescherm)
        self.root.add_widget(self.instellingenscherm)
        
        self.check_of_credentials_al_bestaan()
        
        return self.root
    
    def check_of_credentials_al_bestaan(self):
        keyring = JsonStore("keyring.json")
        
        try:
            ## Ze bestaan wel
            gebruikersnaam = keyring.get("kotnetcli")["gebruikersnaam"]
            wachtwoord     = keyring.get("kotnetcli")["wachtwoord"]
            
            print "----------------"
            print "Gebruikersnaam: " + gebruikersnaam
            print "Wachtwoord:     " + wachtwoord
            print "----------------"
            print "--> Opgehaald."
            
            
            self.instellingenscherm.ids["opslaanvergeetknop"].toestand = "vergeten"
            self.instellingenscherm.ids["opslaanvergeetknop"].text = "Gebruikersnaam en wachtwoord opnieuw instellen"
            self.instellingenscherm.ids["opslaanvergeetknop"].background_color = [2.5, 1, 1, 1]
            self.instellingenscherm.ids["veld_gebruikersnaam"].disabled = True
            self.instellingenscherm.ids["veld_wachtwoord"].disabled = True
            self.instellingenscherm.ids["veld_gebruikersnaam"].text = gebruikersnaam
            self.instellingenscherm.ids["veld_wachtwoord"].text = wachtwoord
            self.instellingenscherm.ids["veld_gebruikersnaam"].font_size = 120
            
        except KeyError:
            ## Ze bestaan nog niet
            print "Gebruikersnaam en wachtwoord zijn onbekend."
            #self.menuscherm.ids["inlogknop"].disabled = True
            #self.menuscherm.ids["uitlogknop"].disabled = True
        
    def ga_naar_actiescherm_en_log_in(self):
        self.root.current = "actie"
        t = threading.Thread(target=self.actiescherm.inloggen)
        t.start()
    
    def ga_naar_actiescherm_en_log_uit(self):
        self.root.current = "actie"
        self.actiescherm.uitloggen()
    

if __name__ == '__main__':
    KotnetApp().run()
