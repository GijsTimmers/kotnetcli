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
import socket
import threading
import mechanize

from kivy.app import App
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard       ## HTML opslaan in clipboard ter ondersteuning
from kivy.storage.jsonstore import JsonStore

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from pygments.lexers import TextLexer


class AppCredentials():
    def __init__(self):
        self.keyring = JsonStore("keyring.json")
    
    def print_credentials(self, gebruikersnaam, wachtwoord, msg):
        print "----------------"
        print "Gebruikersnaam: " + gebruikersnaam
        print "Wachtwoord:     " + wachtwoord
        print "----------------"
        print "--> " + msg
        
    def getCreds(self):
        try:
            gebruikersnaam = self.keyring.get("kotnetcli")["gebruikersnaam"]
            wachtwoord     = self.keyring.get("kotnetcli")["wachtwoord"]
            
            self.print_credentials(gebruikersnaam, wachtwoord, "opgehaald uit keyring.json")
        
            ## return credentials als een tweedelige tuple
            return (gebruikersnaam, wachtwoord)
        
        except KeyError:
            print "Gebruikersnaam en wachtwoord zijn onbekend."
            return None
    
    def setCreds(self, gebruikersnaam, wachtwoord):
        self.keyring.put("kotnetcli", \
                    gebruikersnaam = gebruikersnaam, \
                    wachtwoord     = wachtwoord)
        self.print_credentials(gebruikersnaam, wachtwoord, "opgeslagen in keyring.json")
    
    def forgetCreds(self):
        self.keyring.delete("kotnetcli")
        self.print_credentials("????????", "????????", "verwijderd uit keyring.json")

class AppCommunicator():
    def __init__(self, Scherm):
        self.scherm = Scherm
        
        ## De zgn. "lexer" definiëren voor het outputvak: de lexer is de module
        ## die de code in het outputvak inleest, en op basis van de ingestelde
        ## programmeertaal een kleur geeft. Omdat dat bij ons niet gewenst is,
        ## stellen we de lexer in op TextLexer(), waardoor alle tekst hier
        ## dezelfde kleur krijgt.
        self.scherm.ids["outputvak"].lexer = TextLexer()
        
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
    
    def print_wait(self, msg):
        ## Werkt iets anders dan in een terminal: backspaces zijn niet mogelijk
        ## om de boel te overschrijven. Daarom printen we niets als [WAIT],
        ## we gebruiken alleen een [ OK ] bij succes en een [FAIL] bij falen.
        self.scherm.ids["outputvak"].text += msg

    ## Encapsulates the printing of a "succes" string on display
    ## Override this method to change the appearance of the printed string.
    def print_success(self):
        self.scherm.ids["outputvak"].text += "[ OK ]\n"

    ## Encapsulates the printing of a "fail" string on display
    ## Override this method to change the appearance of the printed string.
    def print_fail(self):
        self.scherm.ids["outputvak"].text += "[FAIL]\n"
    
    def print_voortgangsbalk(self, waarde):
        self.scherm.ids["voortgangsbalk"].value = waarde
    
    def eventGetCredentialsStart(self):
        self.print_wait("Gegevens ophalen........... ")
    def eventGetCredentialsSuccess(self):
        self.print_success()
    def eventGetCredentialsFailure(self):
        self.print_fail()
        
    
    def eventKotnetVerbindingStart(self):
        self.print_wait("Kotnetverbinding testen.... ")
    def eventKotnetVerbindingSuccess(self):
        self.print_success()
        self.print_voortgangsbalk(20)
    def eventKotnetVerbindingFailure(self):
        self.print_fail()
    
    def eventNetloginStart(self):
        self.print_wait("Netlogin openen............ ")
    def eventNetloginSuccess(self):
        self.print_success()
        self.print_voortgangsbalk(40)
    def eventNetloginFailure(self):
        self.print_fail()
        
    def eventKuleuvenStart(self):
        self.print_wait("KU Leuven kiezen........... ")
    def eventKuleuvenSuccess(self):
        self.print_success()
    def eventKuleuvenFailure(self):
        self.print_fail()

    def eventInvoerenStart(self):
        self.print_wait("Gegevens invoeren.......... ")
    def eventInvoerenSuccess(self):
        self.print_success()
        self.print_voortgangsbalk(60)
    def eventInvoerenFailure(self):
        self.print_fail()

    def eventOpsturenStart(self):
        self.print_wait("Gegevens opsturen.......... ")
    def eventOpsturenSuccess(self):
        self.print_success()
        self.print_voortgangsbalk(80)
    def eventOpsturenFailure(self):
        self.print_fail()
        
    def eventLoginGeslaagd(self, downloadpercentage, uploadpercentage):
        self.print_voortgangsbalk(100)
        self.scherm.ids["outputvak"].text += "Download:  " + self.print_balk(downloadpercentage) + "\n"
        self.scherm.ids["outputvak"].text += "Upload:    " + self.print_balk(uploadpercentage)   + "\n"
    def eventLoginFailure(self, msg):
        self.scherm.ids["outputvak"].text += "Fout bij inloggen: " + msg
        



class AppBrowser():
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.addheaders = [("User-agent", "Firefox")]
    def bevestig_kotnetverbinding(self):
        ## try to open a TCP connection on port 443 with a maximum waiting time
        try:
            BROWSER_TIMEOUT_SEC = 1.5
            sock = socket.create_connection(("netlogin.kuleuven.be", 443), BROWSER_TIMEOUT_SEC)
            sock.close()
            return True
        except:
            return False
    
    def login_open_netlogin(self):
        response = self.browser.open("https://netlogin.kuleuven.be/cgi-bin/wayf2.pl?inst=kuleuven&lang=nl&submit=Ga+verder+%2F+Continue", \
        timeout=1.5)
        
    def login_input_credentials(self, cr):
        (gebruikersnaam, wachtwoord) = cr.getCreds()
        self.browser.select_form(nr=1)
        self.browser.form["uid"] = gebruikersnaam
        wachtwoordvaknaam = \
        self.browser.form.find_control(type="password").name
        self.browser.form[wachtwoordvaknaam] = wachtwoord
    
    def login_send_credentials(self):
        self.browser.submit()

    ## This method parses the server's response. On success, it returns a tuple of
    ## length 2: (downloadpercentage, uploadpercentage); else it raises an
    ## appropriate exception
    def login_parse_results(self):
        html = unicode(self.browser.response().read(), "utf-8")
        #print html
        #print "---------------------------------------------"
        #print "---------------------------------------------"
        #print "---------------------------------------------"
        
        ## Parsen gaat wél op PC, niet op Android: bs4 conflicteert met mechanize
        ## rond een bepaalde library, die ze allebei nodig hebben.
        ## Workaround: parsen met re ipv bs4.
        
        rccode = int(re.findall("(?<=\<!-- \<rc=)\d+", html)[0])
        print "RC=" + str(rccode)
        
        ## login rc codes contained in the response html page
        RC_LOGIN_SUCCESS            = 100
        RC_LOGIN_INVALID_USERNAME = 201
        RC_LOGIN_INVALID_PASSWORD = 202
        RC_LOGIN_MAX_IP             = 206

        if rccode == RC_LOGIN_SUCCESS:
            ## downloadpercentage parsen
            downstring       = re.findall("(?<=available download = )\d+ of \d+", html)[0]
            downverbruikt    = float(re.findall("\d+", downstring)[0])
            downtotaal       = float(re.findall("\d+", downstring)[1])
            downpercentage   = int(round(downverbruikt/downtotaal * 100))
            
            ## uploadpercentage parsen
            upstring         = re.findall("(?<=available upload = )\d+ of \d+", html)[0]
            upverbruikt      = float(re.findall("\d+", upstring)[0])
            uptotaal         = float(re.findall("\d+", upstring)[1])
            uppercentage     = int(round(upverbruikt/uptotaal * 100))
        
            print downpercentage
            print uppercentage
            return (downpercentage, uppercentage)
        
        elif (rccode == RC_LOGIN_INVALID_USERNAME) or \
            (rccode == RC_LOGIN_INVALID_PASSWORD):
            raise WrongCredentialsException()
        
        elif rccode == RC_LOGIN_MAX_IP:
            raise MaxNumberIPException()
            
        else:
            raise UnknownRCException(rccode, html)

## Appendix bij AppBrowser(): globale exceptionklassen aanmaken. Kan helaas
## niet worden gesubclasst.

class WrongCredentialsException(Exception):
    pass

##TODO hier het ip address in opslaan (~ hieronder de rccode)
class MaxNumberIPException(Exception):
    pass
    
class UnknownRCException(Exception):
    def __init__(self, rccode, html):
        self.rccode = rccode
        self.html = html

    def get_info(self):
        return (self.rccode, self.html)
        
class AppWorker():
    ## Stuurt het hele loginproces aan via AppCredentials(), AppBrowser()
    ## en AppCommunicator().
    def __init__(self, Scherm):
        self.scherm = Scherm
        self.cr     = AppCredentials()
        self.co     = AppCommunicator(self.scherm)
        self.br     = AppBrowser()
    
    def inloggen(self):
        ## Voert alle stappen uit, die nodig zijn om in te loggen.
        
        ## In tegenstelling tot de gewone kotnetcli kunnen we hier geen sys.exit()
        ## gebruiken om de worker te doen stoppen: de app zou dan crashen. Daar-
        ## om zetten we de stappen gewoon achter elkaar, en gebruiken we steeds
        ## return-statements om de uitvoering voortijdig af te breken bij problemen.
                
        
    
        #### --------< Verbinding testen >-------- ####
        self.co.eventKotnetVerbindingStart()
        if self.br.bevestig_kotnetverbinding():
            self.co.eventKotnetVerbindingSuccess()
        else:
            self.co.eventKotnetVerbindingFailure()
            return
    
        #### --------< Netlogin openen >-------- ####
        self.co.eventNetloginStart()
        try:
            self.br.login_open_netlogin()
            self.co.eventNetloginSuccess()
        except:
            self.co.eventNetloginFailure()
            return
    
        #### --------< Gegevens invoeren >-------- ####
        self.co.eventInvoerenStart()
        try:
            ## Credentials meegeven als object. Geeft een exception als
            ## het inloggen niet lukt (bijvoorbeeld bij een lege keyring)
            self.br.login_input_credentials(self.cr)
            self.co.eventInvoerenSuccess()
        except:
            self.co.eventInvoerenFailure()
            return
            
        #### --------< Gegevens opsturen >-------- ####
        self.co.eventOpsturenStart()
        try:
            self.br.login_send_credentials()
            self.co.eventOpsturenSuccess()
        except:
            self.co.eventOpsturenFailure()
            return
        
        #### --------< Resultaten parsen >-------- ####
        ## geen self.co.*Start() bij parsen uiteraard
        try:
            downpercentage, uppercentage = self.br.login_parse_results()
            self.co.eventLoginGeslaagd(downpercentage, uppercentage)
        except WrongCredentialsException:
            self.co.eventLoginFailure("Controleer uw logingegevens.")
        except MaxNumberIPException:
            self.co.eventLoginFailure("Maximaal aantal logins bereikt.")
        except UnknownRCException as unknownexception:
            ## HTML naar klembord kopiëren voor ondersteuning
            #print Clipboard.get_types()
            Clipboard.put(unknownexception.get_info()[1].encode("utf-8"), "STRING")
            #print Clipboard.get("STRING")
            self.co.eventLoginFailure("Onbekende fout. HTML opgeslagen in klembord. Neem contact op met de ontwikkelaars.")
            
        
        ## Thread eindigt nu vanzelf, want er is niks meer te doen.


class MenuScreen(Screen):
    ## Moet blijven staan. Als je deze (schijnbaar lege) klasse verwijdert,
    ## werkt het menuscherm niet meer. De eienlijke inhoud staat in het
    ## .kv-bestand.
    pass

class ActionScreen(Screen):
    def inloggen(self):
        ## Bij het inloggen geven we self mee aan de AppWorker. self is in dit
        ## geval dus het actiescherm zelf. De AppWorker heeft deze nodig
        ## om berichten op te tonen.
        ## Merk op dat deze methode niets anders doet dan de Worker aanroepen.
        ## Wordt gedraaid als thread door KotnetApp().ga_naar_actiescherm_en_log_in()
        wr = AppWorker(self)
        wr.inloggen()
        #AppWorker().inloggen(self)

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
            self.ids["opslaanvergeetknop"].font_size = 30
            self.ids["opslaanvergeetknop"].text = "Controleer uw gegevens en klik opnieuw."
        else:
            ## Als alles klopt, slaan we het op in de keyring.
            keyring = JsonStore("keyring.json")
            keyring.put("kotnetcli", \
                        gebruikersnaam = gebruikersnaam, \
                        wachtwoord     = wachtwoord)
            print "--> Opgeslagen in keyring.json."
            
            self.ids["opslaanvergeetknop"].toestand = "vergeten"
            self.ids["opslaanvergeetknop"].font_size = 30
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
        self.ids["opslaanvergeetknop"].font_size = 50
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
        self.cr = AppCredentials()
        
        try:
            gebruikersnaam, wachtwoord = self.cr.getCreds()
                        
            self.instellingenscherm.ids["opslaanvergeetknop"].toestand = "vergeten"
            self.instellingenscherm.ids["opslaanvergeetknop"].text = "Gebruikersnaam en wachtwoord opnieuw instellen"
            self.instellingenscherm.ids["opslaanvergeetknop"].background_color = [2.5, 1, 1, 1]
            self.instellingenscherm.ids["veld_gebruikersnaam"].disabled = True
            self.instellingenscherm.ids["veld_wachtwoord"].disabled = True
            self.instellingenscherm.ids["veld_gebruikersnaam"].text = gebruikersnaam
            self.instellingenscherm.ids["veld_wachtwoord"].text = wachtwoord
            self.instellingenscherm.ids["veld_gebruikersnaam"].font_size = 120
            
        except TypeError:
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
