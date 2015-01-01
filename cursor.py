#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cursor.py
#  
#  Copyright 2015 Gijs <gijs@therion>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import os

def hide():
    if os.name == "posix":
        ## Hide the terminal cursor using ANSI escape codes
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
            
    if os.name == "nt":
        import msvcrt
        import ctypes

        class _CursorInfo(ctypes.Structure):
            _fields_ = [("size", ctypes.c_int),
                        ("visible", ctypes.c_byte)]

        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


def show():
    if os.name == "posix":
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
    
    elif os.name == "nt":
        import msvcrt
        import ctypes
        
        class _CursorInfo(ctypes.Structure):
            _fields_ = [("size", ctypes.c_int),
                        ("visible", ctypes.c_byte)]
                        
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    
