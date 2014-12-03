#!/bin/sh
# -*- coding: utf-8 -*-

if [ -d "pyinstaller" ]; then
    echo "OK, pyinstaller aanwezig..."
#fi

#if [ ! -d "pyinstaller" ]; then
else
    echo "pyinstaller afwezig, gaat nu clonen..."
    git clone https://github.com/pyinstaller/pyinstaller.git
fi

./pyinstaller/pyinstaller.py compile-lin.spec &&\
cp -v dist/kotnetcli . &&\
echo "Compileren succesvol."



