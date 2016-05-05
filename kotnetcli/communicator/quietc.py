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

#TODO find an elegant way to make the dots optional for subclasses (eg dialogc)
STD_MSG_TEST        = "Kotnetverbinding testen...."
STD_MSG_GET         = "Gegevens ophalen..........."
STD_MSG_POST        = "Gegevens opsturen.........."
STD_MSG_PROCESS     = "Gegevens verwerken........."
STD_MSG_DOWNLOAD    = "Download: {down}%"
STD_MSG_UPLOAD      = "Upload:   {upl}%"

STD_ERR_OFFLINE     = "Connection attempt to netlogin service '{srv}' timed out. Are you on the kotnet network?"
STD_ERR_CREDS       = "Uw logingegevens kloppen niet. Gebruik kotnetcli --forget om deze te resetten."
STD_ERR_INST        = "Uw gekozen institutie '{inst}' klopt niet. Gebruik kotnetcli --institution om een andere institutie te kiezen."
STD_ERR_MAX_IP      = "U bent al ingelogd op een ander IP-adres. Gebruik kotnetcli --force-login om u toch in te loggen."
STD_ERR_RC          = "De netlogin server geeft een onbekende rc-code '{rc}' terug. Contacteer de kotnetcli developers om ondersteuning te krijgen."
STD_ERR_RC_INFO     = "====== START HTML DUMP ======\n{html}====== END HTML DUMP ======"
STD_ERR_SRV         = "De netlogin server rapporteert een 'internal script error'. Probeer opnieuw in te loggen..."
STD_ERR_PANIC       = "Internal kotnetcli exception."
STD_ERR_PANIC_INFO  = "====== TRACEBACK BELOW ======\n{trace_str}====== END OF TRACEBACK ======"

class QuietCommunicator(object):
    
    def __init__(self):
        pass

    ################## APPEARANCE HELPER METHODS ##################
    ## these can be overridden to easily change appearance of subclass communicators
    
    def print_info(self, str):
        pass
    
    def print_err(self, str):
        pass
    
    ################## COMMUNICATOR INTERFACE ##################
    
    def eventExit(self):
        pass

    def eventCheckNetworkConnection(self):
        self.print_info(STD_MSG_TEST)
    
    def eventGetData(self):
        self.print_info(STD_MSG_GET)
    
    def eventPostData(self):
        self.print_info(STD_MSG_POST)
    
    def eventProcessData(self):
        self.print_info(STD_MSG_PROCESS)

    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.print_info(STD_MSG_DOWNLOAD.format(down=downloadpercentage))
        self.print_info(STD_MSG_UPLOAD.format(upl=uploadpercentage))
    
    def eventFailureOffline(self, srv):
        self.print_err(STD_ERR_OFFLINE.format(srv=srv))
    
    def eventFailureCredentials(self):
        self.print_err(STD_ERR_CREDS)
    
    def eventFailureMaxIP(self):
        self.print_err(STD_ERR_MAX_IP)
    
    def eventFailureInstitution(self, inst):
        self.print_err(STD_ERR_INST.format(inst=inst))
        
    def eventFailureServerScriptError(self):
        self.print_err(STD_ERR_SRV)
    
    def eventFailureUnknownRC(self, rccode, html):
        self.print_err(STD_ERR_RC.format(rc=rccode))
        self.print_info(STD_ERR_RC_INFO.format(html=html))
    
    def eventFailureInternalError(self, traceback):
        self.print_err(STD_ERR_PANIC)
        self.print_info(STD_ERR_PANIC_INFO.format(trace_str=traceback.format_exc()))

## end class QuietCommunicator
