#!/usr/bin/python 

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout



def scherm():
    
    b = BoxLayout(orientation="vertical")
        
    bnrtitle = Label(text="kotnetcli", font_size=30, size_hint_y=None, height=60)
    bnrsubtitle = Label(text="by Gijs Timmers and Jo van Bulck", font_size=14, size_hint_y=None, height=30)
    
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
