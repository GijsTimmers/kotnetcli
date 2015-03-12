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
from browser import KotnetBrowser
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
    
    def worker1(self):
        self.status = "bezig"
        self.kb = KotnetBrowser()
        self.kb.login_open_netlogin()
        self.ids["outputvak"].text = "Netlogin openen.......... [ OK ]\n"
        self.status = "klaar"
    
    def worker2(self):
        class creds():
            def getCreds(self):
                keyring = JsonStore("keyring.json")
                gebruikersnaam = keyring.get("kotnetcli")["gebruikersnaam"]
                wachtwoord     = keyring.get("kotnetcli")["wachtwoord"]
                
                print "----------------"
                print "Gebruikersnaam: " + gebruikersnaam
                print "Wachtwoord:     " + wachtwoord
                print "----------------"
                print "--> Opgehaald."
                
                return (gebruikersnaam, wachtwoord)
            
        self.kb.login_input_credentials(creds())
        self.ids["outputvak"].text += "Gegevens invoeren........ [ OK ]\n"
    
    def worker3(self):
        self.kb.login_send_credentials()
        self.ids["outputvak"].text += "Gegevens opsturen........ [ OK ]\n"
        
        ## Parsen gaat wél op PC, niet op Android: bs4 conflicteert met mechanize
        ## rond een bepaalde library, die ze allebei nodig hebben.
        ## Workaround: parsen met iets anders dan bs4.
        
        #(up, down) = self.kb.login_parse_results()
        
        #self.ids["outputvak"].text += "Download:            [" + str(down) + "%]\n"
        #self.ids["outputvak"].text += "Upload:              [" + str(up)   + "%]\n"
        #self.ids["outputvak"].text += "Download " + self.print_balk(down) + "\n"
        #self.ids["outputvak"].text += "Upload   " + self.print_balk(up)   + "\n"
    
    def inloggen_go(self, dt):
        self.status = "klaar"
        thread = threading.Thread(target=self.worker1)
        thread.start()
        thread.join()
        thread = threading.Thread(target=self.worker2)
        thread.start()
        thread.join()
        thread = threading.Thread(target=self.worker3)
        thread.start()
        
        #Clock.schedule_once(self.worker1)
        #Clock.schedule_once(self.worker2)
        #Clock.schedule_once(self.worker3)
        #event = Clock.create_trigger(self.worker1)
        #event()
        #event = Clock.create_trigger(self.worker2)
        #event()
        #event = Clock.create_trigger(self.worker3)
        #event()
        """
        self.ids["outputvak"].lexer = TextLexer()
                
        self.kb = KotnetBrowser()
        self.kb.login_open_netlogin()
        self.ids["outputvak"].text = "Netlogin openen.......... [ OK ]\n"
    
    
        class creds():
            def getCreds(self):
                keyring = JsonStore("keyring.json")
                gebruikersnaam = keyring.get("kotnetcli")["gebruikersnaam"]
                wachtwoord     = keyring.get("kotnetcli")["wachtwoord"]
                
                print "----------------"
                print "Gebruikersnaam: " + gebruikersnaam
                print "Wachtwoord:     " + wachtwoord
                print "----------------"
                print "--> Opgehaald."
                
                return (gebruikersnaam, wachtwoord)
            
        self.kb.login_input_credentials(creds())
        self.ids["outputvak"].text += "Gegevens invoeren........ [ OK ]\n"
    
    
        self.kb.login_send_credentials()
        self.ids["outputvak"].text += "Gegevens opsturen........ [ OK ]\n"
        
        (up, down) = self.kb.login_parse_results()
        
        #self.ids["outputvak"].text += "Download:            [" + str(down) + "%]\n"
        #self.ids["outputvak"].text += "Upload:              [" + str(up)   + "%]\n"
        self.ids["outputvak"].text += "Download " + self.print_balk(down) + "\n"
        self.ids["outputvak"].text += "Upload   " + self.print_balk(up)   + "\n"
        """
    
    def inloggen(self):
        Clock.schedule_once(self.inloggen_go, 0)
        
    """
    def inloggen(self):
        def update_tekst(*args):
            self.af_te_drukken_tekst = (
            "Netlogin openen..... [ OK ]", \
            "Netlogin openen..... [ OK ]\nGegevens invoeren... [ OK ]", \
            "Netlogin openen..... [ OK ]\nGegevens invoeren... [ OK ]\nGegevens opsturen... [ OK ]", \
            "Netlogin openen..... [ OK ]\nGegevens invoeren... [ OK ]\nGegevens opsturen... [ OK ]\nDownload:            [ 82%]\nUpload:              [100%]"
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
    """
    def uitloggen(self):
        print "Ik wil uitloggen."

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
        self.actiescherm.inloggen()
    
    def ga_naar_actiescherm_en_log_uit(self):
        self.root.current = "actie"
        self.actiescherm.uitloggen()
    
    
    """
    def on_pause(self):
        ## Here you can save data if needed
        return True

    def on_resume(self):
        ## Here you can check if any data needs replacing (usually nothing)
        pass
    """
        

if __name__ == '__main__':
    KotnetApp().run()
