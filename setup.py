#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

## Dependencies:    python-mechanize, python-keyring, curses
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

#from distutils.core import setup
from setuptools import setup

setup(
  name = "kotnetcli",
  packages = ["kotnetcli"], # this must be the same as the name above
  version = "1.3.0",
  description = "An easy automated way to log in on Kotnet",
  author = "Gijs Timmers and Jo Van Bulck",
  author_email = "gijs.timmers@student.kuleuven.be",
  url = "https://github.com/GijsTimmers/kotnetcli", # use the URL to the github repo
  download_url = "https://github.com/GijsTimmers/kotnetcli/releases/tag/1.3.0", # I'll explain this in a second
  keywords = ["kotnet", "login", "kotnetlogin", "leuven", "kuleuven"], # arbitrary keywords
  install_requires=[
          "mechanize",
          "keyring",
          "notify2",
          "colorama",
          "python2-pythondialog",
          "beautifulsoup4"
                    ],
  classifiers = [],
  entry_points = {
              "console_scripts": [
                  "kotnetcli = kotnetcli:kotnetcli",
                                 ],
                  },
)
