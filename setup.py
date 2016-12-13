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

from setuptools import setup, find_packages
from kotnetcli import __version__, __src_url__
import os

## Only essential dependencies should be listed here. Specific communicator
## dependencies can always be installed later, if desired.
dependencies = [
    "argcomplete",
    "argparse",
    "logging",
    "cursor",
    "keyring",
    "keyrings.alt",
    "requests",
    "beautifulsoup4"
]

setup(
    name = "kotnetcli",
    packages = find_packages(),
    version = __version__,
    description = "An easy automated way to log in on Kotnet",
    author = "Gijs Timmers and Jo Van Bulck",
    author_email = "gijs.timmers@student.kuleuven.be",
    url = __src_url__,
    keywords = ["kotnet", "login", "kotnetlogin", "leuven", "kuleuven"],
    install_requires = dependencies,
    entry_points = {
        "console_scripts":[
            "kotnetcli=kotnetcli.kotnetcli:main",
            #TODO dedicated test command deprecated with kotnetsrv
            "kotnetsrv=kotnetcli.server.server:main"
        ],
        "gui_scripts":[
            "kotnetgui=kotnetcli.kotnetgui:main"
        ],
    },
    classifiers=[]
)
