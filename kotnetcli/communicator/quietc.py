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
STD_INST_PROMPT     = "Kies uw institutie [default=kuleuven]"
STD_MSG_INST_CHOICE = "Geldige KotNet instituties zijn: "

STD_MSG_TEST        = "Kotnetverbinding testen"
STD_MSG_GET         = "Gegevens ophalen"
STD_MSG_POST        = "Gegevens opsturen"
STD_MSG_PROCESS     = "Gegevens verwerken"
STD_MSG_DOWNLOAD    = "Download: {down}%"
STD_MSG_UPLOAD      = "Upload:   {upl}%"
STD_MSG_FORGET      = "Credentials verwijderen"

STD_ERR_INPUT       = "Ongeldige invoer."
STD_ERR_OFFLINE     = "Connection attempt to netlogin service '{srv}' timed out. Are you on the kotnet network?"
STD_ERR_CREDS       = "Uw logingegevens kloppen niet. Gebruik kotnetcli --forget om deze te resetten."
STD_ERR_INST        = "Uw gekozen institutie '{inst}' klopt niet. Gebruik kotnetcli --institution om een andere institutie te kiezen."
STD_ERR_MAX_IP      = "U bent al ingelogd op een ander IP-adres. Gebruik kotnetcli --force-login om u toch in te loggen."
STD_ERR_RC          = "De netlogin server geeft een onbekende rc-code '{rc}' terug. Contacteer de kotnetcli developers om ondersteuning te krijgen."
STD_ERR_INFO_RC     = "====== START HTML DUMP ======\n{html}====== END HTML DUMP ======"
STD_ERR_SRV         = "De netlogin server rapporteert een 'internal script error'. Probeer opnieuw in te loggen..."
STD_ERR_FORGET      = "You have already removed your kotnetcli credentials."
STD_ERR_PANIC       = "Internal kotnetcli exception. Contacteer de kotnetcli developers om ondersteuning te krijgen."
STD_ERR_INFO_PANIC  = "====== TRACEBACK BELOW ======\n{trace}====== END OF TRACEBACK ======"

class QuietCommunicator(object):
    
    def __init__(self, inst_dict):
        self.msg_width      = STD_MSG_WIDTH
        
        self.user_prompt    = STD_USERNAME_PROMPT
        self.pwd_prompt     = STD_PWD_PROMPT
        self.inst_prompt    = STD_INST_PROMPT
        self.msg_inst       = STD_MSG_INST_CHOICE
        self.inst_dict      = inst_dict
        
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
        self.err_input      = STD_ERR_INPUT

    ################## APPEARANCE HELPER METHODS ##################
    ## override to easily change appearance of subclasses
    
    def fmt_info(self, info):
        return info.ljust(self.msg_width, '.')
    
    def fmt_err(self, err):
        return err
    
    def fmt_err_info(self, info):
        return info
    
    def fmt_prompt_msg(self, msg):
        return ":: " + msg
    
    def fmt_prompt(self, string):
        return self.fmt_prompt_msg(string) + " > "
    
    def fmt_input_choice(self, key, val, maxKeyLen):
        return "    {k:{width}} {v}".format(k=key, v=val, width=maxKeyLen+1)

    ################## EVENT HELPER METHODS ##################
    ## simplified communicator event categories for subclasses
    
    def eventInfo(self, info):
        pass

    def eventError(self, err):
        pass

    def eventErrorInfo(self, info):
        pass

    ################## PRIVATE HELPER WRAPPERS ##################
    ## not meant to be overridden by subclass communicators
    
    def doEventInfo(self, info):
        self.eventInfo(self.fmt_info(info))
    
    def doEventError(self, err):
        self.eventError(self.fmt_err(err))
    
    def doEventErrorInfo(self, info):
        self.eventErrorInfo(self.fmt_err_info(info))
    
    ################## INPUT HELPER METHODS ##################
    
    def get_input(self, prompt_str, accept=lambda x: x, pwd=False):
        prompt = self.fmt_prompt(prompt_str)
        while True:
            rv = getpass.getpass(prompt) if pwd else raw_input(prompt)
            rv = rv.strip()
            if accept(rv): break
            print(self.fmt_err(self.err_input))
        return rv
    
    def display_input_choices(self, msg, d):
        print(self.fmt_prompt_msg(msg))
        maxKeyLen = max(len(k) for k in d.keys())
        for k, v in d.items():
            print(self.fmt_input_choice(k, v, maxKeyLen))
    
    ################## COMMUNICATOR INTERFACE ##################
    
    def eventPromptCredentials(self):
        self.display_input_choices(self.msg_inst, self.inst_dict)
        inst = self.get_input(self.inst_prompt,
                              lambda x: x in self.inst_dict.keys())
        user = self.get_input(self.user_prompt)
        pwd  = self.get_input(self.pwd_prompt, pwd=True)
        return (user, pwd, inst)
    
    def eventExit(self):
        pass

    def eventCheckNetworkConnection(self):
        self.doEventInfo(self.msg_test)
    
    def eventGetData(self):
        self.doEventInfo(self.msg_get)
    
    def eventPostData(self):
        self.doEventInfo(self.msg_post)
    
    def eventProcessData(self):
        self.doEventInfo(self.msg_process)

    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.doEventInfo(self.msg_download.format(down=downloadpercentage))
        self.doEventInfo(self.msg_upload.format(upl=uploadpercentage))
    
    def eventForgetCreds(self):
        self.doEventInfo(self.msg_forget)
    
    def eventForgetCredsSuccess(self):
        pass
    
    def eventFailureOffline(self, srv):
        self.doEventError(self.err_offline.format(srv=srv))
    
    def eventFailureCredentials(self):
        self.doEventError(self.err_creds)
    
    def eventFailureMaxIP(self):
        self.doEventError(self.err_ip)
    
    def eventFailureInstitution(self, inst):
        self.doEventError(self.err_inst.format(inst=inst))
        
    def eventFailureServerScriptError(self):
        self.doEventError(self.err_srv)
    
    def eventFailureUnknownRC(self, rccode, html):
        self.doEventError(self.err_rc.format(rc=rccode))
        self.doEventErrorInfo(self.err_info_rc.format(html=html))
    
    def eventFailureInternalError(self, traceback_str):
        self.doEventError(self.err_panic)
        self.doEventErrorInfo(self.err_info_panic.format(trace=traceback_str))

    def eventFailureForget(self):
        self.doEventError(self.err_forget)

## end class QuietCommunicator
