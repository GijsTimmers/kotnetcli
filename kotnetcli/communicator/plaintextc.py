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
import cursor

from quietc import QuietCommunicator

class SuperPlaintextCommunicator(QuietCommunicator):

    def __init__(self):
        cursor.hide()
        self.hasFailed = False
    
    ################## APPEARANCE HELPER METHODS ##################

    def print_info(self, str):
        sys.stdout.write(str)
        ## print no trailing newline to be able to update WAIT/OK line status
        #if (self.hasFailed):
        #    sys.stdout.write("\n")
        sys.stdout.flush()
    
    def print_err(self, str):
        self.hasFailed = True
        self.fmt_fail()
        self.finalize_session()
        self.fmt_err(str)

    def fmt_er(self, str):
        print "ERROR::" + str

    def fmt_wait(self):
        print "[WAIT]" + "\b\b\b\b\b\b\b",
        sys.stdout.flush()

    def fmt_success(self):
        print "[ OK ]"

    def fmt_done(self):
        print "[DONE]"

    def fmt_fail(self):
        print "[FAIL]"

    def fmt_generic_bar(self, percentage, style, color, stop_color, stop_style):
        percentagefloat = float(percentage)
        percentagestring = str(percentage)
        lengteVanBalkfloat = 15.0
        lengteVanBalkint = 15
        lengteVanRuimteVoorPercentages = 3
        
        aantalStreepjesObvPercentage = int(round(percentagefloat/100.0 * lengteVanBalkfloat))
        print style + "[" + color + \
        "=" * aantalStreepjesObvPercentage + stop_color + \
        " " * (lengteVanBalkint-aantalStreepjesObvPercentage) + \
        "][" + \
        " " * (lengteVanRuimteVoorPercentages - len(percentagestring)) + \
        color + percentagestring + "%" + \
        stop_color + "]" + stop_style

    def fmt_bar(self, percentage):
        self.fmt_generic_bar(percentage, "", "", "", "")

    def finalize_session(self, success):
        pass

    ################## COMMON LOGIN/LOGOUT COMMUNICATOR INTERFACE ##################

    def eventExit(self):
        cursor.show()

    def eventCheckNetworkConnection(self):
        super(SuperPlaintextCommunicator, self).eventCheckNetworkConnection()
        self.fmt_wait()
    
    def eventGetData(self):
        self.fmt_success()
        super(SuperPlaintextCommunicator, self).eventGetData()
        self.fmt_wait()
    
    def eventPostData(self):
        self.fmt_success()
        super(SuperPlaintextCommunicator, self).eventPostData()
        self.fmt_wait()
        
    def eventProcessData(self):
        self.fmt_success()
        super(SuperPlaintextCommunicator, self).eventProcessData()
        self.fmt_wait()

## end class SuperPlaintextCommunicator

class LoginPlaintextCommunicator(SuperPlaintextCommunicator):
    
    def finalize_session(self):
        self.print_info("Inloggen.................. "),
        if self.hasFailed:
            self.fmt_fail()
        else:
            self.fmt_done()
    
    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.fmt_success()
        self.print_info("Download: ")
        self.fmt_bar(downloadpercentage)
        self.print_info("Upload:   ")
        self.fmt_bar(uploadpercentage)
        self.finalize_session()

## end class LoginPlaintextCommunicator
