#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck
##
## Licence:         GPLv3
##
## kotnetcli is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## kotnetcli is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with kotnetcli.  If not, see <http://www.gnu.org/licenses/>.

import sys
from plaintextc import *

from colorama import (
                      Fore,
                      Style,
                      init as colorama_init
                     )

class SuperColoramaCommunicator(SuperPlaintextCommunicator):

    ################## INITIALIZATION ##################

    def __init__(self):
        self.init_colors(map(lambda x:x.upper(),[ "green", "yellow", "red", "bright" ]))
        colorama_init()
        super(SuperColoramaCommunicator,self).__init__()
    
    def init_colors(self, colorNameList):
        style = getattr(Style, colorNameList.pop())
        err_color = getattr(Fore, colorNameList.pop())
        wait_color = getattr(Fore, colorNameList.pop())        
        ok_color = getattr(Fore, colorNameList.pop())
        self.ERR_COLOR = err_color
        self.ERR_STYLE = style
        self.WAIT_STYLE = style
        self.WAIT_COLOR = wait_color
        self.SUCCESS_STYLE = style
        self.SUCCESS_COLOR = ok_color
        self.FAIL_STYLE = style
        self.FAIL_COLOR = err_color
        self.PERC_STYLE = style
        self.CRITICAL_PERC_COLOR = err_color
        self.LOW_PERC_COLOR = wait_color
        self.OK_PERC_COLOR = ok_color
        
    ################## OVERRIDE PLAINTEXT APPEARANCE METHODS ##################

    def printerr(self, msg):
        sys.stderr.write(self.ERR_STYLE + self.ERR_COLOR),
        super(SuperColoramaCommunicator,self).printerr(msg),
        sys.stderr.write(Style.RESET_ALL),
        sys.stderr.flush()

    def print_wait(self):
        print self.WAIT_STYLE + "[" + self.WAIT_COLOR + \
        "WAIT" + Fore.RESET + "]" + Style.RESET_ALL + "\b\b\b\b\b\b\b",
        sys.stdout.flush()

    def print_success(self):
        print self.SUCCESS_STYLE + "[" + self.SUCCESS_COLOR + " OK " + \
        Fore.RESET + "]" + Style.RESET_ALL

    def print_done(self):
        print self.SUCCESS_STYLE + "[" + self.SUCCESS_COLOR + "DONE" + \
        Fore.RESET + "]" + Style.RESET_ALL

    def print_fail(self):
        print self.FAIL_STYLE + "[" + self.FAIL_COLOR + "FAIL" + \
        Fore.RESET + "]" + Style.RESET_ALL

    ## Overrides the printing of a "balk" string on stdout
    def print_bar(self, percentage):
        if percentage <= 10:
            color = self.CRITICAL_PERC_COLOR
        elif 10 < percentage < 60:
            color = self.LOW_PERC_COLOR
        else:
            color = self.OK_PERC_COLOR
        
        self.print_generic_bar(percentage, self.PERC_STYLE, color, Fore.RESET, Style.RESET_ALL)

class LoginColoramaCommunicator(SuperColoramaCommunicator, LoginPlaintextCommunicator):

    ## no specific login colorama behavior for now
    def dummy(self):
        pass

