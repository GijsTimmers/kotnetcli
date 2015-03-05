#!/usr/bin/python 

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class Schermen():
    def __init__(self):
        print "Laadt de Schermen-klasse in"
        
        self.b = BoxLayout(orientation="vertical")
        
        bnrtitle = Label(text="kotnetcli", font_size=30, size_hint_y=None, height=60)
        bnrsubtitle = Label(text="by Gijs Timmers and Jo van Bulck", font_size=14, size_hint_y=None, height=30)
        
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
