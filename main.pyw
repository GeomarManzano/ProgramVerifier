#! /usr/bin/python

# Author: Geomar Manzano

import sys, os, subprocess
from PyQt4 import QtCore, QtGui

TIMER = 5000

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Central Widget
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create actions for the main window and the menus
        self.createActions()
        self.createMenus()

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage('No entered program', TIMER)

        # Necessary Widgets
        self.programLabel = QtGui.QLabel('&Program')
        self.inputTxtLabel = QtGui.QLabel('&Text File')
        self.programButton = QtGui.QPushButton('Browse')
        self.inputTxtButton = QtGui.QPushButton('Browse')
        self.runButton = QtGui.QPushButton('&Run')
        
        # Buddies
        self.programLabel.setBuddy(self.programButton)
        self.inputTxtLabel.setBuddy(self.inputTxtButton)

        # Initializations
        self.initUI()
        self.initConnections()
    def createActions(self):
        self.onScreen_action = QtGui.QAction('On Screen', self, checkable=True,
                                             triggered=self.onScreen_slot)
        self.offScreen_action = QtGui.QAction('Text File', self, checkable=True,
                                              triggered=self.offScreen_slot)

        # Managing the set of checkable actions for the output mode and
        # ensures that if one of the actions is to set on, then the rest are
        # set to off
        self.outputModeGroup = QtGui.QActionGroup(self)
        self.outputModeGroup.addAction(self.onScreen_action)
        self.outputModeGroup.addAction(self.offScreen_action)
        self.onScreen_action.setChecked(True)
        
    def createMenus(self):
        self.optionMenu = self.menuBar().addMenu('&Options')
        
        self.outputMenu = self.optionMenu.addMenu('Output Mode')
        self.outputMenu.addAction(self.onScreen_action)
        self.outputMenu.addAction(self.offScreen_action)
    def programOpen_slot(self):
        self.progPath = QtGui.QFileDialog.getOpenFileName(self, 'Open Program')
        self.status.showMessage('Program Loaded', TIMER)
    def fileOpen_slot(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open Program')
        fl = open(fileName, 'r')
        self.status.showMessage('File Loaded', TIMER)
    def execProgram_slot(self):
        subprocess.call(str(self.progPath))
        self.status.showMessage('Program Executed', TIMER)
    def onScreen_slot(self):
        print 'Test: On Screen'
    def offScreen_slot(self):
        print 'Test: Off Screen'
    def initConnections(self):
        self.programButton.clicked.connect(self.programOpen_slot)
        self.inputTxtButton.clicked.connect(self.fileOpen_slot)
        self.runButton.clicked.connect(self.execProgram_slot)
    def initUI(self):
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.runButton)
        
        # Central Widget layout setup
        layout = QtGui.QGridLayout()
        layout.addWidget(self.programLabel, 0, 0)
        layout.addWidget(self.programButton, 0, 1)
        layout.addWidget(self.inputTxtLabel, 1, 0)
        layout.addWidget(self.inputTxtButton, 1, 1)
        layout.addLayout(buttonLayout, 2, 0, 1, 2)
        self.centralWidget.setLayout(layout)

        self.setWindowTitle('Program Verifier')
        self.setFixedSize(250, 140)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) # Required for all PyQt applications
    window = MainWindow()              # Instantiation of the MainWindow class
    window.show()                      # Paint the widgets onto the screen
    sys.exit(app.exec_())              # Exit the program cleanly
