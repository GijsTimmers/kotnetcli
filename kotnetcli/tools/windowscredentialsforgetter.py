#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-keyring
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

import keyring                          ## Voor ophalen wachtwoord
import time                             ## Voor timeout

def vergeetCredentials():
    kr = keyring.get_keyring()
    try:
        kr.delete_password("kotnetcli", "gebruikersnaam")
        kr.delete_password("kotnetcli", "wachtwoord")
        print "---------------------------------------------"
        print "Kotnetcli-logingegevens succesvol verwijderd!"
        print "---------------------------------------------"
    except keyring.errors.PasswordDeleteError:
        print "-------------------------------------------"
        print "Kotnetcli-logingegevens zijn al verwijderd!"
        print "-------------------------------------------"
    finally:
        time.sleep(3)
        

if __name__ == '__main__':
    vergeetCredentials()

