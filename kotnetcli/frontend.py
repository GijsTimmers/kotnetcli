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
import argparse
import argcomplete
import logging

from .worker import (
    EXIT_FAILURE,
    EXIT_SUCCESS
)

from .communicator.fabriek import (
    inst_dict
)

from .tools import log
logger = logging.getLogger(__name__)

from __init__ import __version__, __release_name__, __src_url__, __descr__

## Class encapsulating common CLI arguments for all binaries in the kotnetcli
## distribution.
## NOTE inherit from "object" to be able to use super() in child classes.
class AbstractFrontEnd(object):

    def __init__(self, descr):
        estr = "return values:\n  {}\t\t\ton success\n  {}\t\t\ton failure"
        estr = estr.format(EXIT_SUCCESS, EXIT_FAILURE)
        self.parser = argparse.ArgumentParser(description=descr,
            epilog=estr, formatter_class=argparse.RawDescriptionHelpFormatter, 
            conflict_handler='resolve')
        self.addGeneralFlags()

    def addGeneralFlags(self):
        self.parser.add_argument("-v", "--version", action=PrintVersionAction,
            help="show program's version number and exit", nargs=0)
        self.parser.add_argument("-l", "--license", action=PrintLicenceAction,
            help="show license info and exit", nargs=0)

        ## Debug flag with optional (nargs=?) level; defaults to 
        ## LOG_LEVEL_DEFAULT if option not present; defaults to debug if option
        ## present but no level specified.
        self.parser.add_argument("--debug", help="specify the debug verbosity",
            nargs="?", const="debug", metavar="LEVEL",
            choices=[ 'critical', 'error', 'warning', 'info', 'debug' ],
            action="store", default=log.LOG_LEVEL_DEFAULT)
        self.parser.add_argument("--time", action="store_true",
            help="include fine-grained timing info in logger output")

    def parseArgs(self):
        ## Call argcomplete to complete flags automatically when using bash.
        argcomplete.autocomplete(self.parser)
        
        ## Parse CLI arguments corresponding to self.parser.
        argumenten = self.parser.parse_args()
        self.init_debug_level(argumenten.debug, argumenten.time)
        logger.debug("parse_args() is: %s", argumenten)
        return argumenten

    def init_debug_level(self, log_level, include_time):
        try:
            log.init_logging(log_level, include_time)
        except ValueError:
            print("{}: Invalid debug level: {}".format(self.cmd, log_level))
            exit(EXIT_FAILURE)

## end class AbstractFrontEnd

class AbstractClientFrontEnd(AbstractFrontEnd):

    def __init__(self):
        super(AbstractClientFrontEnd, self).__init__(__descr__)
        self.addNetworkFlags()

    def addNetworkFlags(self):
        self.parser.add_argument("--institution", action="store", default=None,
            metavar="INST", choices=inst_dict.keys(),
            help="override the instititution")
        self.parser.add_argument("-L", "--localhost", action="store_true",
            help="connect to the localhost development test server")

## end class AbstractClientFrontEnd

logo = """   __
 __\ \                 {cmd} v{version} - '{release}'
 \ \\\_\___             Copyright (C) 2014-2017 Kotnetcli Development Team
  \   V  / __          <{github_url}>
   \  `\<</ /
    \  _\_\<<          This program may be freely redistributed under
     \_\ `_\_\         the terms of the GNU General Public License.
        \_\\
"""

class PrintVersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(logo.format(cmd=parser.prog, version=__version__, 
            release=__release_name__, github_url=__src_url__))
        exit(EXIT_SUCCESS)

license = """{cmd}: {descr}
Copyright (C) 2014-2017 Kotnetcli Development Team
<{github_url}>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kotnetcli.  If not, see <https://www.gnu.org/licenses/>.
"""

class PrintLicenceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(license.format(cmd=parser.prog, github_url=__src_url__,
            descr=__descr__))
        exit(EXIT_SUCCESS)

