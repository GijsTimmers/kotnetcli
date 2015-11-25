#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To  view a copy of
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View,
## CA 94042, USA.

from setuptools import setup, find_packages
import os

 
dependencies = [
		"argcomplete",
		"cursor",
		"keyring",
		"notify2",
		"requests",
		"colorama",
		"python2-pythondialog",
		"beautifulsoup4"
				  ]

## notify2 can't be used on Windows.
if os.name == "nt":
    dependencies.remove("notify2")

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
        "console_scripts": ["kotnetcli=kotnetcli:main"]},
  include_package_data = True
)
