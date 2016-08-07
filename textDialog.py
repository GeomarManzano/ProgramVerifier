#! /usr/bin/python

# Author: Geomar Manzano

import sys
from PyQt4 import QtCore, QtGui

# Possibly add the feature that allows the results to be saved via File -> Save # if the user wishes to later on
class TextDialog(QtGui.QDialog):
    def __init__(self, title='', txt ='', parent=None):
        super(TextDialog, self).__init__(parent)
        self.text = QtGui.QTextEdit()
        self.initUI()
        self.initConnections()
        self.setWindowTitle(title)
        self.text.setText(txt)
    def initUI(self):
        self.text.setReadOnly(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)
    def initConnections(self):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dlg = TextDialog('Test', 'This is a dialog used only for showing text')
    dlg.show()
    sys.exit(app.exec_())
