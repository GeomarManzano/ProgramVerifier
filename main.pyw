#! /usr/bin/python

# Author: Geomar Manzano

import sys, os
from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        centralWidget = QtGui.QWidget()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Program Verifier')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
