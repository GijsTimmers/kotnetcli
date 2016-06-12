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

from quietc import QuietCommunicator

import logging
logger = logging.getLogger(__name__)

class LoggerCommunicator(QuietCommunicator):

    ## do not left-adjust progress info
    def fmt_info(self, info):
        return info

    def eventInfo(self, info):
        logger.info(info)

    def eventError(self, err):
        logger.error(err)

    def eventErrorInfo(self, info):
        logger.info(info)