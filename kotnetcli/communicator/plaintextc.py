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
        pass

    def do_failure(self, err_str):
        self.print_fail()
        self.finalize_session(False)
        self.printerr(err_str)

    ################## COMMON LOGIN/LOGOUT COMMUNICATOR INTERFACE ##################

    def eventExit(self):
        cursor.show()

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

    def eventFailureOffline(self, srv):
        err_str = "Connection attempt to netlogin service '{}' timed out. Are you on the kotnet network?".format(srv)
        self.do_failure(err_str)

    def eventFailureCredentials(self):
        err_str = "Uw logingegevens kloppen niet. Gebruik kotnetcli --forget om deze te resetten."
        self.do_failure(err_str)
    
    def eventFailureInstitution(self, inst):
        err_str = "Uw gekozen institutie '{}' klopt niet. Gebruik kotnetcli --institution om een andere institutie te kiezen.".format(inst)
        self.do_failure(err_str)
        
    def eventFailureServerScriptError(self):
        err_str = "De netlogin server rapporteert een 'internal script error'. Probeer opnieuw in te loggen..."
        self.do_failure(err_str)
    
    def eventFailureUnknownRC(self, rccode, html):
        err_str = "De netlogin server geeft een onbekende rc-code '{}' terug. Contacteer de kotnetcli developers om ondersteuning te krijgen.".format(rccode)
        self.do_failure(err_str)
        self.print_txt("====== START HTML DUMP ======\n")
        self.print_txt(html)
        self.print_txt("====== END HTML DUMP ======\n")
    
    def eventFailureInternalError(self, traceback):
        err_str = "Internal kotnetcli exception: traceback below."
        self.do_failure(err_str)
        self.print_txt(traceback.format_exc())

class LoginPlaintextCommunicator(SuperPlaintextCommunicator):
    
    ################## LOGIN COMMUNICATOR INTERFACE ##################

    def finalize_session(self, success):
        self.print_txt("Inloggen................... "),
        if success:
            self.print_done()
        else:
            self.print_fail()
    
    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.print_success()
        self.print_txt("Download:  ")
        self.print_bar(downloadpercentage)
        self.print_txt("Upload:    ")
        self.print_bar(uploadpercentage)
        self.finalize_session(True)

    def eventFailureMaxIP(self):
        err_str = "U bent al ingelogd op een ander IP-adres. Gebruik kotnetcli --force-login om u toch in te loggen."
        self.do_failure(err_str)
