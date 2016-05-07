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
import threading
import logging
from PyQt4 import QtGui, QtCore
from Queue import Queue

from .communicator.summaryc import AbstractSummaryCommunicator
from .credentials import KeyRingCredentials
from .worker import (
    DummyLoginWorker,
    EXIT_FAILURE,
    EXIT_SUCCESS
)
from .tools import log

## we use a queue to synchronize the background netlogin thread, requesting the
## credentials from the GUICredentialsDialog in the main thread
queue = Queue()

logger = logging.getLogger(__name__)

## Main GUI class displaying progress of the netlogin thread
## TODO this should be subclassed in login/logout classes
class KotnetGUI(QtGui.QWidget):
    
    def __init__(self, title):
        super(KotnetGUI, self).__init__()
        self.initUI(title)

    def initUI(self, title):
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)

        self.text = QtGui.QTextEdit()
        self.text.setReadOnly(True)
        ## cross-platform monospace font (see http://stackoverflow.com/a/1835938)
        font = QtGui.QFont("Monospace")
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.text.setFont(font)
        vbox.addWidget(self.text)
        
        grid = QtGui.QGridLayout()
        lblDown = QtGui.QLabel("Download")
        grid.addWidget(lblDown, 1, 0)
        self.downloadbar = QtGui.QProgressBar()
        grid.addWidget(self.downloadbar, 1, 1)
        
        lblUpl = QtGui.QLabel("Upload")
        grid.addWidget(lblUpl, 2, 0)
        self.uploadbar = QtGui.QProgressBar()
        grid.addWidget(self.uploadbar, 2, 1) 
        vbox.addLayout(grid)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        self.okButton = QtGui.QPushButton("OK")
        self.okButton.setEnabled(False)
        self.okButton.clicked.connect(self.close)
        hbox.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        hbox.addWidget(self.cancelButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)    
        
        self.resize(375, 250)
        self.setWindowTitle(title)    
        self.show()

    def finalize(self):
        self.okButton.setEnabled(True)
        self.cancelButton.setEnabled(False)

    def updateText(self, msg):
        self.text.append(msg)

    def updateError(self, err):
        self.text.setTextColor(QtCore.Qt.red)
        self.text.append(err)
        self.finalize()

    def updatePercentages(self, download, upload):
        self.downloadbar.setValue(download)
        self.uploadbar.setValue(upload)
        self.finalize()

    def queryCredentials(self):
        logger.debug("spawning GUICredentialsDialog")
        d = GUICredentialsDialog(self)
        d.exec_()
        logger.debug("queuing result from GUICredentialsDialog")
        queue.put(d.getCreds())

## end class KotnetGUI

## Helper GUI class for a pop-up dialog querying credentials from the user
class GUICredentialsDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(GUICredentialsDialog, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        
        grid = QtGui.QGridLayout()
        lblUser = QtGui.QLabel("Username")
        grid.addWidget(lblUser, 1, 0)
        self.user = QtGui.QLineEdit()
        grid.addWidget(self.user, 1, 1)
        
        lblPwd = QtGui.QLabel("Password")
        grid.addWidget(lblPwd, 2, 0)
        self.pwd = QtGui.QLineEdit()
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        grid.addWidget(self.pwd, 2, 1) 
        vbox.addLayout(grid)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        okButton = QtGui.QPushButton("OK")
        okButton.clicked.connect(self.accept)
        hbox.addWidget(okButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)    
        
        self.resize(250, 100)
        self.setWindowTitle("Input credentials")    
        self.show()
    
    def getCreds(self):
        return (self.user.text(), self.pwd.text())
   
## end class GUICredentialsDialog

## Helper GUI class for a pop-up dialog querying initial login/logout choice
class GUIOptionDialog(QtGui.QDialog):

    def __init__(self):
        super(GUIOptionDialog, self).__init__()
        self.initUI()
        
    def initUI(self):
        grid = QtGui.QGridLayout()
        
        vbox = QtGui.QVBoxLayout()
        lblWhat = QtGui.QLabel("<b>What do you want to do?  </b>")
        vbox.addWidget(lblWhat)
        self.rbIn = QtGui.QRadioButton("KotNet Login")
        self.rbIn.setChecked(True)
        vbox.addWidget(self.rbIn)
        self.rbOut = QtGui.QRadioButton("KotNet Logout")
        vbox.addWidget(self.rbOut)
        grid.addLayout(vbox, 0, 0)
        
        lblLogo = QtGui.QLabel()
        logo = QtGui.QPixmap("kotnetcli/tools/logo_small.jpg")
        scaledLogo = logo.scaled(QtCore.QSize(120,120), QtCore.Qt.KeepAspectRatio)
        lblLogo.setPixmap(scaledLogo)
        grid.addWidget(lblLogo, 0, 1)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        okButton = QtGui.QPushButton("OK")
        okButton.clicked.connect(self.accept)
        hbox.addWidget(okButton)
        grid.addLayout(hbox, 1, 0)
        
        self.setLayout(grid)
        self.resize(250, 100)
        self.setWindowTitle("Welcome to kotnetcli")    
        self.show()
    
    def getChoice(self):
        return "login" if self.rbIn.isChecked() else "logout"
    
    
## end class GUIOptionDialog

## Custom communicator translating netlogin progress to Qt signals for the GUI thread
class LoginGUICommunicator(AbstractSummaryCommunicator):

    GUI_TEXT_LJUST_WIDTH = 26

    def __init__(self, textSignal, errorSignal, percentagesSignal, credsSignal):
        super(LoginGUICommunicator, self).__init__()
        self.msg_width = self.GUI_TEXT_LJUST_WIDTH
        self.updateGUIText = textSignal
        self.updateGUIError = errorSignal
        self.updateGUIPercentages = percentagesSignal
        self.credsSignal = credsSignal

    #TODO worker should request creds from communicator if none in creds object
    def eventAskCredentials(self):
        self.updateGUIText.emit("Credentials opvragen.... ")
        self.credsSignal.emit()
        logger.debug("block waiting on credentialsDialog queue")
        (u,p) = queue.get()
        logger.debug("got credentials for user '{}'".format(u))
        return (u,p)

    def print_info(self, str):
        self.updateGUIText.emit(str)
    
    def print_err(self, str):
        self.updateGUIError.emit("ERROR::" + str)

    def eventLoginSuccess(self, downloadpercentage, uploadpercentage):
        self.updateGUIPercentages.emit(downloadpercentage, uploadpercentage)

## end class LoginGUICommunicator

## Entry point class for the kotnetcli background netlogin thread
class KotnetcliRunner(QtCore.QObject):

    ## Qt signals used to link communicator with GUI thread
    ## note: must be a class attribute of a QObject class
    updateGUIText = QtCore.pyqtSignal(str)
    updateGUIError = QtCore.pyqtSignal(str)
    updateGUIPercentages = QtCore.pyqtSignal(int,int)
    GUIQueryCredentials = QtCore.pyqtSignal()

    def do_netlogin(self):
        logger.debug("creating netlogin kotnetcli objects")
        co = LoginGUICommunicator(self.updateGUIText, self.updateGUIError,
                                 self.updateGUIPercentages, self.GUIQueryCredentials)
        creds = KeyRingCredentials()
        worker = DummyLoginWorker("kuleuven", 1, True, False, 100)
        #co.eventAskCredentials()
        worker.go(co, creds)

## end class KotnetcliRunner

## main method creating GUI and spawning a kotnetcli runner thread
def main():
    log.init_logging("debug", False)

    app = QtGui.QApplication(sys.argv)
    
    logger.debug("spawning GUIOptionDialog")
    d = GUIOptionDialog()
    d.exec_()
    choice = d.getChoice()
    if (choice != "login"):
        logger.error("'{}' currently not supported in kotnetgui beta".format(choice))
        sys.exit(EXIT_FAILURE)    
    
    logger.debug("creating GUI objects")
    gui = KotnetGUI("kotnetcli network login")
    runner = KotnetcliRunner()
    runner.updateGUIText.connect(gui.updateText)
    runner.updateGUIError.connect(gui.updateError)
    runner.updateGUIPercentages.connect(gui.updatePercentages)
    runner.GUIQueryCredentials.connect(gui.queryCredentials)

    logger.info("starting netlogin thread")
    kotnetcliThread = threading.Thread(target=runner.do_netlogin)
    ## any running daemon threads are killed automatically on program exit
    kotnetcliThread.daemon = True
    kotnetcliThread.start()
    
    logger.info("starting GUI main thread")
    app.exec_()
    logger.info("GUI main thread returned; exiting")
    sys.exit(EXIT_SUCCESS)
    
