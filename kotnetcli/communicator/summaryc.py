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

from loggerc import LoggerCommunicator

SUMMARY_MSG_LOGIN       = "Login geslaagd."
SUMMARY_MSG_DOWN_UP     = "Download: {downl}%, Upload: {upl}%"
SUMMARY_MSG_FORGET      = "Credentials successfully removed."

SUMMARY_ERR_OFFLINE     = "Connection attempt timed out."
SUMMARY_ERR_CREDS       = "Invalid credentials."
SUMMARY_ERR_INST        = "Invalid institution '{inst}'."
SUMMARY_ERR_MAX_IP      = "Maximum IP logins reached."
SUMMARY_ERR_RC          = "Unknown rc-code '{rc}'."
SUMMARY_ERR_FORGET      = "Credentials already removed."
SUMMARY_ERR_SRV         = "Internal server script error."
SUMMARY_ERR_PANIC       = "Internal kotnetcli exception."

class AbstractSummaryCommunicator(LoggerCommunicator):
    
    def __init__(self):
        super(AbstractSummaryCommunicator, self).__init__()
    
        self.err_offline    = SUMMARY_ERR_OFFLINE
        self.err_creds      = SUMMARY_ERR_CREDS
        self.err_inst       = SUMMARY_ERR_INST
        self.err_ip         = SUMMARY_ERR_MAX_IP
        self.err_rc         = SUMMARY_ERR_RC
        self.err_forget     = SUMMARY_ERR_FORGET
        self.err_srv        = SUMMARY_ERR_SRV
        self.err_panic      = SUMMARY_ERR_PANIC
    
    def print_err(self, string):
        print("ERROR::" + string)

class ForgetSummaryCommunicator(AbstractSummaryCommunicator, LoggerCommunicator):
    def eventForgetCredsSuccess(self):
        print SUMMARY_MSG_FORGET
    
class LoginSummaryCommunicator(AbstractSummaryCommunicator, LoggerCommunicator):

    def eventLoginSuccess(self, download, upload):
        print SUMMARY_MSG_LOGIN
        print SUMMARY_MSG_DOWN_UP.format(downl=download, upl=upload)
