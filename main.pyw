#! /usr/bin/python

# Author: Geomar Manzano

import sys, os
from PyQt4 import QtCore, QtGui

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
        status = self.statusBar()
        status.showMessage('Filler Text')

        # Necessary Widgets
        self.programLabel = QtGui.QLabel('&Program')
        self.inputTxtLabel = QtGui.QLabel('&Text File')
        self.programButton = QtGui.QPushButton('Browse')
        self.inputTxtButton = QtGui.QPushButton('Browse')

        # Buddies
        self.programLabel.setBuddy(self.programButton)
        self.inputTxtLabel.setBuddy(self.inputTxtButton)

        # Initializations
        self.initUI()
        self.initConnections()
    def createActions(self):
        pass
    def createMenus(self):
        pass
    def fileOpen_slot(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        print 'Opened:', name  # Testing purposes
    def initConnections(self):
        self.programButton.clicked.connect(self.fileOpen_slot)
        self.inputTxtButton.clicked.connect(self.fileOpen_slot)
    def initUI(self):
        # Central Widget layout setup
        layout = QtGui.QGridLayout()
        layout.addWidget(self.programLabel, 0, 0)
        layout.addWidget(self.programButton, 0, 1)
        layout.addWidget(self.inputTxtLabel, 1, 0)
        layout.addWidget(self.inputTxtButton, 1, 1)
        self.centralWidget.setLayout(layout)

        self.setWindowTitle('Program Verifier')
        self.setMinimumSize(250, 100)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) # Required for all PyQt applications
    window = MainWindow()              # Instantiation of the MainWindow class
    window.show()                      # Paint the widgets onto the screen
    sys.exit(app.exec_())              # Exit the program cleanly
