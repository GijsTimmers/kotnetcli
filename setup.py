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
from kotnetcli import __version__, __src_url__, __descr__, resolve_path
import os

## Only essential dependencies should be listed here. Specific communicator
## dependencies can always be installed later, if desired.
dependencies = [
    "argcomplete",
    "argparse",
    "logging",
    "cursor",
    "colorama",
    "keyring",
    "keyrings.alt",
    "requests",
    "beautifulsoup4"
]

## Create a custom .desktop file for the kotnetgui binary
kotnetgui_desktop_template = """[Desktop Entry]
Version={version}
Name=KotnetGUI
Comment={descr}
Exec=kotnetgui
Icon={icon_path}
Terminal=false
Type=Application
Categories=Utility;
"""

f = open("build/kotnetgui.desktop", "w")
f.write(kotnetgui_desktop_template.format(version=__version__, descr=__descr__,
    ##TODO scalable icon + portable path
    icon_path=resolve_path("/usr/share/icons/kotnetcli.jpg")))
f.close()

setup(
    name = "kotnetcli",
    packages = find_packages(),
    version = __version__,
    description = __descr__, 
    author = "Gijs Timmers and Jo Van Bulck",
    author_email = "gijs.timmers@student.kuleuven.be",
    url = __src_url__,
    keywords = ["kotnet", "login", "kotnetlogin", "leuven", "kuleuven"],
    install_requires = dependencies,
    entry_points = {
        "console_scripts":[
            "kotnetcli=kotnetcli.kotnetcli:main",
            "kotnetsrv=kotnetcli.server.server:main"
        ],
        "gui_scripts":[
            "kotnetgui=kotnetcli.kotnetgui:main"
        ],
    },
    package_data = {
        "kotnetcli":["data/logo_small.jpg","server/cgi-bin/*"]
    },
    data_files = [
        ("bitmaps", ["kotnetcli/data/kotnetcli.jpg"]),
        ("cgi-bin", ["kotnetcli/server/cgi-bin/netlogin.pl",
                     "kotnetcli/server/cgi-bin/wayf2.pl"]),
        ("/usr/share/applications/", [f.name]),
        ("/usr/share/icons/", ["kotnetcli/data/kotnetcli.jpg"])
        ],
    include_package_data = True,
    classifiers=[]
)


