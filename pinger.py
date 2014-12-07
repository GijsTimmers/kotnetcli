#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import os
import sys
import subprocess

def ping(co):    
    if os.name == "posix":
        with open(os.devnull, 'w') as dev_null:
            if subprocess.call(["ping", "-c", "1", "-w", "1", "netlogin.kuleuven.be"], \
            stdout=dev_null, stderr=dev_null) == 0:
                ## 0 staat voor een exit code van True van het ping-commando.
                if subprocess.call(["ping", "-c", "1", "-w", "1", "toledo.kuleuven.be"], \
                stdout=dev_null, stderr=dev_null) == 0:
                    ## we zijn al online
                    co.eventPingAlreadyOnline()
                    co.beeindig_sessie()
                    sys.exit(1)
                else:
                    ## we moeten nog inloggen
                    co.eventPingSuccess()
            else:
                ## geen netwerkverbinding
                co.eventPingFailure()
                co.beeindig_sessie()
                sys.exit(1)
    
    elif os.name == "nt":
        with open("NUL", 'w') as dev_null:
            if subprocess.call(["ping", "-n", "1", "-w", "1", "netlogin.kuleuven.be"], \
            stdout=dev_null, stderr=dev_null) == 0:
                ## 0 staat voor een exit code van True van het ping-commando.
                if subprocess.call(["ping", "-c", "1", "-w", "1", "toledo.kuleuven.be"], \
                stdout=dev_null, stderr=dev_null) == 0:
                    ## we zijn al online
                    co.eventPingAlreadyOnline()
                    co.beeindig_sessie()
                    sys.exit(1)
                else:
                    ## we moeten nog inloggen
                    co.eventPingSuccess()
            else:
                ## geen netwerkverbinding
                co.eventPingFailure()
                co.beeindig_sessie()
                sys.exit(1)
