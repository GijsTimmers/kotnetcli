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
from .error_codes import *

class SuperPlaintextCommunicator(QuietCommunicator):
    def __init__(self):
        self.offline_msg = "Connection attempt to netlogin service failed. Are you on the kotnet network?"
        self.creds_msg   = "Uw logingegevens kloppen niet. Gebruik kotnetcli --forget om deze te resetten."
        self.max_ip_msg  = "U bent al ingelogd op een ander IP-adres. Gebruik kotnetcli --force-login om u toch in te loggen."
        self.inst_msg    = "Uw gekozen institutie klopt niet. Gebruik kotnetcli --institution om een andere institutie te kiezen."
        self.script_msg  = "De kotnet server rapporteert een 'internal script error'. Probeer opnieuw in te loggen..."
        self.rc_msg      = "De kotnet server geeft een onbekende rc-code terug. Contacteer de kotnetcli developers om ondersteuning te krijgen."
        self.panic_msg   = "Internal kotnetcli exception: traceback below."
        cursor.hide()

    ################## APPEARANCE HELPER METHODS ##################
    ## override these to change appearance of subclass terminal-based communicators

    def printerr(self, msg):
        sys.stderr.write("ERROR::" + msg + "\n"),
        sys.stderr.flush()

    def print_txt(self, msg):
        sys.stdout.write(msg)

    def print_wait(self):
        print "[WAIT]" + "\b\b\b\b\b\b\b",
        sys.stdout.flush()

    def print_success(self):
        print "[ OK ]"

    def print_done(self):
        print "[DONE]"

    def print_fail(self):
        print "[ FAIL ]"

    def print_generic_bar(self, percentage, style, color, stop_color, stop_style):
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

    def print_bar(self, percentage):
        self.print_generic_bar(percentage, "", "", "", "")

    def finalize_session(self, success):
        cursor.show()

    ################## COMMON LOGIN/LOGOUT COMMUNICATOR INTERFACE ##################

    def eventCheckNetworkConnection(self):
        self.print_txt("Kotnetverbinding testen.... ")
        self.print_wait()
    
    def eventGetData(self):
        self.print_success()
        self.print_txt("Gegevens ophalen........... ")
        self.print_wait()
    
    def eventPostData(self):
        self.print_success()
        self.print_txt("Gegevens opsturen.......... ")
        self.print_wait()
        
    def eventProcessData(self):
        self.print_success()
        self.print_txt("Gegevens verwerken......... ")
        self.print_wait()

    def eventFailure(self, code):
        self.print_fail()
        ## fail gracefully
        self.finalize_session(False)
        ## provide the user with an appropriate error message
        if code == KOTNETCLI_SERVER_OFFLINE:
            self.printerr(self.offline_msg)
        elif code == KOTNETCLI_SERVER_WRONG_CREDS:
            self.printerr(self.creds_msg)
        elif code == KOTNETCLI_SERVER_MAX_IP:
            self.printerr(self.max_ip_msg)
        elif code == KOTNETCLI_SERVER_INVALID_INSTITUTION:
            self.printerr(self.inst_msg)
        elif code == KOTNETCLI_SERVER_SCRIPT_ERROR:
            self.printerr(self.script_msg)
        elif code == KOTNETCLI_SERVER_UNKNOWN_RC:
            self.printerr(self.rc_msg)
        else:
            self.printerr(self.panic_msg)

class LoginPlaintextCommunicator(SuperPlaintextCommunicator):
    
    ################## LOGIN COMMUNICATOR INTERFACE ##################
    
    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.print_success()
        self.print_txt("Download:  ")
        self.print_bar(downloadpercentage)
        self.print_txt("Upload:    ")
        self.print_bar(uploadpercentage)
        self.finalize_session(True)
        
    def finalize_session(self, success):
        self.print_txt("Inloggen................... "),
        if success:
            self.print_done()
        else:
            self.print_fail()
        super(LoginPlaintextCommunicator, self).finalize_session(success)
