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

import getpass

STD_MSG_WIDTH       = 26

STD_USERNAME_PROMPT = "Voer uw s-nummer/r-nummer in"
STD_PWD_PROMPT      = "Voer uw wachtwoord in"
STD_INST_PROMPT     = "Kies uw institutie [kuleuven, kuleuven-campusnet, kotnetext]"

STD_MSG_TEST        = "Kotnetverbinding testen"
STD_MSG_GET         = "Gegevens ophalen"
STD_MSG_POST        = "Gegevens opsturen"
STD_MSG_PROCESS     = "Gegevens verwerken"
STD_MSG_DOWNLOAD    = "Download: {down}%"
STD_MSG_UPLOAD      = "Upload:   {upl}%"
STD_MSG_FORGET      = "Credentials verwijderen"

STD_ERR_OFFLINE     = "Connection attempt to netlogin service '{srv}' timed out. Are you on the kotnet network?"
STD_ERR_CREDS       = "Uw logingegevens kloppen niet. Gebruik kotnetcli --forget om deze te resetten."
STD_ERR_INST        = "Uw gekozen institutie '{inst}' klopt niet. Gebruik kotnetcli --institution om een andere institutie te kiezen."
STD_ERR_MAX_IP      = "U bent al ingelogd op een ander IP-adres. Gebruik kotnetcli --force-login om u toch in te loggen."
STD_ERR_RC          = "De netlogin server geeft een onbekende rc-code '{rc}' terug. Contacteer de kotnetcli developers om ondersteuning te krijgen."
STD_ERR_INFO_RC     = "====== START HTML DUMP ======\n{html}====== END HTML DUMP ======"
STD_ERR_SRV         = "De netlogin server rapporteert een 'internal script error'. Probeer opnieuw in te loggen..."
STD_ERR_FORGET      = "You have already removed your kotnetcli credentials."
STD_ERR_PANIC       = "Internal kotnetcli exception. Contacteer de kotnetcli developers om ondersteuning te krijgen."
STD_ERR_INFO_PANIC  = "====== TRACEBACK BELOW ======\n{trace_str}====== END OF TRACEBACK ======"

class QuietCommunicator(object):
    
    def __init__(self, msg_width=STD_MSG_WIDTH):
        self.msg_width      = msg_width
        
        self.user_prompt    = STD_USERNAME_PROMPT
        self.pwd_prompt     = STD_PWD_PROMPT
        self.inst_prompt    = STD_INST_PROMPT
        
        self.msg_test       = STD_MSG_TEST
        self.msg_get        = STD_MSG_GET
        self.msg_post       = STD_MSG_POST
        self.msg_process    = STD_MSG_PROCESS
        self.msg_download   = STD_MSG_DOWNLOAD
        self.msg_upload     = STD_MSG_UPLOAD
        self.msg_forget     = STD_MSG_FORGET
        
        self.err_offline    = STD_ERR_OFFLINE
        self.err_creds      = STD_ERR_CREDS
        self.err_inst       = STD_ERR_INST
        self.err_ip         = STD_ERR_MAX_IP
        self.err_rc         = STD_ERR_RC
        self.err_info_rc    = STD_ERR_INFO_RC
        self.err_srv        = STD_ERR_SRV
        self.err_forget     = STD_ERR_FORGET
        self.err_panic      = STD_ERR_PANIC
        self.err_info_panic = STD_ERR_INFO_PANIC

    ################## APPEARANCE HELPER METHODS ##################
    ## these can be overridden to easily change appearance of subclass communicators
    
    def get_prompt(self, string):
        return string + " > "
    
    def print_info(self, string):
        pass
    
    def print_err(self, string):
        pass
    
    def print_err_info(self, string):
        pass
    
    def ljust_msg(self, string):
        return string.ljust(self.msg_width, '.')
    
    ################## COMMUNICATOR INTERFACE ##################
    
    def promptCredentials(self):
        inst = raw_input(self.get_prompt(self.inst_prompt))
        user = raw_input(self.get_prompt(self.user_prompt))
        pwd = getpass.getpass(prompt=self.get_prompt(self.pwd_prompt))
        return (user, pwd, inst)
    
    def eventForgetCreds(self):
        self.print_info(self.ljust_msg(self.msg_forget))
    
    def eventForgetCredsSuccess(self):
        pass

    def eventFailureForget(self):
        self.print_err(self.err_forget)    
    
    def eventExit(self):
        pass

    def eventCheckNetworkConnection(self):
        self.print_info(self.ljust_msg(self.msg_test))
    
    def eventGetData(self):
        self.print_info(self.ljust_msg(self.msg_get))
    
    def eventPostData(self):
        self.print_info(self.ljust_msg(self.msg_post))
    
    def eventProcessData(self):
        self.print_info(self.ljust_msg(self.msg_process))

    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.print_info(self.msg_download.format(down=downloadpercentage))
        self.print_info(self.msg_upload.format(upl=uploadpercentage))
    
    def eventFailureOffline(self, srv):
        self.print_err(self.err_offline.format(srv=srv))
    
    def eventFailureCredentials(self):
        self.print_err(self.err_creds)
    
    def eventFailureMaxIP(self):
        self.print_err(self.err_ip)
    
    def eventFailureInstitution(self, inst):
        self.print_err(self.err_inst.format(inst=inst))
        
    def eventFailureServerScriptError(self):
        self.print_err(self.err_srv)
    
    def eventFailureUnknownRC(self, rccode, html):
        self.print_err(self.err_rc.format(rc=rccode))
        self.print_err_info(self.err_info_rc.format(html=html))
    
    def eventFailureInternalError(self, traceback):
        self.print_err(self.err_panic)
        self.print_err_info(self.err_info_panic.format(trace_str=traceback.format_exc()))

## end class QuietCommunicator
