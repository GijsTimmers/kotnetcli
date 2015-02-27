#!/usr/bin/env bash
# -*- coding: utf-8 -*-

mkdir -p -v /tmp/gedeeld
cp -rv ~/Scripts/kotnetcli/* /tmp/gedeeld/

VBoxManage startvm "win7" --type headless
VBoxManage --nologo guestcontrol "win7" execute --image "C:\\users\\gijs\\Desktop\\compileer_easy.bat" --username "gijs" --password "inlog" --wait-exit --wait-stdout
VBoxManage controlvm "win7" savestate

cp -rv /tmp/gedeeld/dist/kotnetcli-win-easy.exe ~/Scripts/kotnetcli/compilation/dist
#rm -rf /tmp/gedeeld
