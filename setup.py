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
import os

 
dependencies = [
		"argcomplete",
		"cursor",
		"keyring",
                "keyrings.alt",
		"notify2",
		"requests",
		"colorama",
		"python2-pythondialog",
		"beautifulsoup4"
				  ]

def check_requirements():

    #assert sys.version_info >= (3, 4), "Please use Python 3.4 or higher."
    
    if os.name == "posix":
        assert os.geteuid() == 0, "Please run with root privileges."


## notify2 can't be used on Windows.
if os.name == "nt":
    dependencies.remove("notify2")

try:
    check_requirements()
    setup(
        name = "kotnetcli",
        packages = ["kotnetcli"],
        version = "1.3.0",
        description = "An easy automated way to log in on Kotnet",
        author = "Gijs Timmers and Jo Van Bulck",
        author_email = "gijs.timmers@student.kuleuven.be",
        url = "https://github.com/GijsTimmers/kotnetcli",
        keywords = ["kotnet", "login", "kotnetlogin", "leuven", "kuleuven"],
        install_requires = dependencies,
      classifiers = [],
      entry_points = {
            "console_scripts": ["kotnetcli=kotnetcli:main",
                                "kotnetcli-dummy=kotnetcli.kotnetcli_test:dummy_main"]},
      include_package_data = True
    )
except AssertionError as e:
    print(e)
