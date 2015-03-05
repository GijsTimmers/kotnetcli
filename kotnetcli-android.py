#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To  view a copy of
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View,
## CA 94042, USA.

import kivy
kivy.require('1.0.9')
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.app import App
import mechanize

from worker import LoginWorker, EXIT_FAILURE
from credentials import KeyRingCredentials
from communicator.fabriek import LoginCommunicatorFabriek

import sys
import time
import traceback

Builder.load_string('''
<HelloWorldScreen>:
    cols: 1
    Label:
        text: 'kotnetcli rocks! kotnetgui sucks!'
    Button:
        text: 'Number of vulnerabilities found in kotnetgui: %d' % root.counter
        on_release: root.my_callback()
''')

class HelloWorldScreen(GridLayout):
    counter = NumericProperty(0)
    def my_callback(self):
        print 'Aangeklikt.'
        self.counter += 1

class HelloWorldApp(App):
    def build(self):
        return HelloWorldScreen()

if  __name__ =='__main__':
    HelloWorldApp().run()
    print "Start nu."
    
    ## create necessary back-end objects
    fab = LoginCommunicatorFabriek()
    co = fab.createPlaintextCommunicator()
    creds = KeyRingCredentials()
    creds.saveGuestCreds("s0204964", "w4chtw00rd")
    
    worker = LoginWorker()
    
    ## execute login
    try:
        worker.go(co, creds)
    except SystemExit, e:
        exit_code = e.code
    except Exception, e:
        exit_code = EXIT_FAILURE
    sys.exit(exit_code)
    



    
