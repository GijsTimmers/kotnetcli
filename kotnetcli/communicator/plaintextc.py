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

class AbstractPlaintextCommunicator(QuietCommunicator):

    def __init__(self, title):
        super(AbstractPlaintextCommunicator, self).__init__()
        cursor.hide()
        
        self.OK_STR     = " OK "
        self.WAIT_STR   = "WAIT"
        self.FAIL_STR   = "FAIL"
        self.ERR_STR    = "ERROR::{err_msg}"
        self.DONE_STR   = "DONE"
        self.FINAL_STR  = self.ljust_msg(title)
    
    ################## APPEARANCE HELPER METHODS ##################

    def print_info(self, string):
        ## print no trailing newline to be able to update WAIT/OK line status
        sys.stdout.write(string + " ")
        sys.stdout.flush()
    
    def print_err(self, string):
        self.fmt_fail()
        self.finalizeSession(fail=True)
        self.fmt_err(string)

    def print_err_info(self, string):
        print(string)

    def fmt_err(self, string):
        print(self.ERR_STR.format(err_msg=string))

    def fmt_wait(self):
        sys.stdout.write("[" + self.WAIT_STR + "]" + "\b" * (2+len(self.WAIT_STR)))
        sys.stdout.flush()

    def fmt_success(self):
        print("[" + self.OK_STR + "]")

    def fmt_done(self):
        print("[" + self.DONE_STR + "]")

    def fmt_fail(self):
        print("[" + self.FAIL_STR + "]")

    # TODO this should be cleaned up
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

    ################## COMMON LOGIN/LOGOUT COMMUNICATOR INTERFACE ##################

    def promptCredentials(self):
        cursor.show()
        (u, pwd) = super(AbstractPlaintextCommunicator, self).promptCredentials()
        cursor.hide()
        return (u, pwd)

    def eventExit(self):
        cursor.show()

    def eventCheckNetworkConnection(self):
        super(AbstractPlaintextCommunicator, self).eventCheckNetworkConnection()
        self.fmt_wait()
    
    def eventGetData(self):
        self.fmt_success()
        super(AbstractPlaintextCommunicator, self).eventGetData()
        self.fmt_wait()
    
    def eventPostData(self):
        self.fmt_success()
        super(AbstractPlaintextCommunicator, self).eventPostData()
        self.fmt_wait()
        
    def eventProcessData(self):
        self.fmt_success()
        super(AbstractPlaintextCommunicator, self).eventProcessData()
        self.fmt_wait()

    def finalizeSession(self, fail=False):
        self.print_info(self.FINAL_STR)
        self.fmt_fail() if fail else self.fmt_done()

## end class AbstractPlaintextCommunicator

class LoginPlaintextCommunicator(AbstractPlaintextCommunicator):
    
    def __init__(self):
        super(LoginPlaintextCommunicator, self).__init__("Inloggen")
    
    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.fmt_success()
        self.print_info("Download:")
        self.fmt_bar(downloadpercentage)
        self.print_info("Upload:  ")
        self.fmt_bar(uploadpercentage)
        self.finalizeSession()

## end class LoginPlaintextCommunicator

class ForgetPlaintextCommunicator(AbstractPlaintextCommunicator):
    
    def __init__(self):
        super(ForgetPlaintextCommunicator, self).__init__("Vergeten")
    
    def eventForgetCreds(self):
        super(ForgetPlaintextCommunicator, self).eventForgetCreds()
        self.fmt_wait()
    
    def eventForgetCredsSuccess(self):
        self.fmt_success()
        self.finalizeSession()
   
## end class ForgetPlaintextCommunicator
