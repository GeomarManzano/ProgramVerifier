#! /usr/bin/python

# Author: Geomar Manzano
 
import sys, subprocess, ntpath
import textDialog
from PyQt4 import QtCore, QtGui

TIMER = 5000 # 5000 milliseconds is equal to 5 seconds

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
        self.loadedProg = QtGui.QLineEdit()
        self.loadedTxtFile = QtGui.QLineEdit()
        self.saveModeLabel = QtGui.QLabel('&Save Mode')
        self.saveModeBox = QtGui.QComboBox()
        self.saveModeBox.addItems(['Overwrite', 'Append'])
        
        # Dialogs
        self.noProgram_errDlg = QtGui.QMessageBox(self)
        
        # Buddies
        self.programLabel.setBuddy(self.programButton)
        self.inputTxtLabel.setBuddy(self.inputTxtButton)
        self.saveModeLabel.setBuddy(self.saveModeBox)

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
        progHead, self.progTail = ntpath.split(str(self.progPath))
        self.loadedProg.setText(self.progTail)
    def fileOpen_slot(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        fl = open(self.fileName, 'r')
        self.status.showMessage('File Loaded', TIMER)
        fileHead, self.fileTail = ntpath.split(str(self.fileName))
        self.loadedTxtFile.setText(self.fileTail)
    def execProgram_slot(self):
        try:
            process = subprocess.Popen(
                [str(self.progPath)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            output, err = process.communicate()
            exit_code = process.wait()

            self.status.showMessage('Program Executed', TIMER)

            if self.onScreen_action.isChecked():
                # Note: replacing self.dlg with dlg will possibly cause dlg
                # to be garbage collected once this method is done executing.
                # Therefore it's required to add the self in to keep the
                # dialog in scope
                self.dlg = textDialog.TextDialog(self.progTail + ' output',
                                                 output)
                
                # Modeless dialog
                self.dlg.show()
            elif self.offScreen_action.isChecked():
                openedFile = open(self.saveFile, self.mode)
                openedFile.write(output)
                openedFile.close()
        except AttributeError:
            self.noProgram_errDlg.critical(self, 'Error', 'No program entered')
    def onScreen_slot(self):
        self.onScreen_action.setChecked(True)
        self.saveMode(False)
    def offScreen_slot(self):
        self.offScreen_action.setChecked(True)
        self.saveFile = QtGui.QFileDialog.getSaveFileName(self, 'Save Results')
        self.saveMode(True)
        self.mode = 'w'      # Save mode is initially overwrite
    def setSaveMode_slot(self, index):
        if index == 0:       # Corresponds to overwrite on the combobox
            self.mode = 'w'
        elif index == 1:     # Corresponds to append on the combox
            self.mode = 'a'
        self.status.showMessage('Save Mode Changed', TIMER)
    def initConnections(self):
        self.programButton.clicked.connect(self.programOpen_slot)
        self.inputTxtButton.clicked.connect(self.fileOpen_slot)
        self.runButton.clicked.connect(self.execProgram_slot)
        self.saveModeBox.currentIndexChanged.connect(self.setSaveMode_slot)
    def initUI(self):
        self.loadedProg.setEnabled(False)
        self.loadedTxtFile.setEnabled(False)
        self.saveMode(False)
        
        # Central Widget layout setup
        layout = QtGui.QGridLayout()
        layout.addWidget(self.programLabel, 0, 0)
        layout.addWidget(self.programButton, 0, 2)
        layout.addWidget(self.loadedProg, 0, 1)
        layout.addWidget(self.inputTxtLabel, 2, 0)
        layout.addWidget(self.inputTxtButton, 2, 2)
        layout.addWidget(self.loadedTxtFile, 2, 1)
        layout.addWidget(self.saveModeLabel, 3, 0)
        layout.addWidget(self.saveModeBox, 3, 1)
        layout.addWidget(self.runButton, 3, 2)
        self.centralWidget.setLayout(layout)

        self.setWindowTitle('Program Verifier')
        self.setFixedSize(400, 150)
    def saveMode(self, isActivated):
        if isActivated:
            self.saveModeBox.setEnabled(True)
            self.saveModeLabel.setEnabled(True)
            self.saveModeBox.setVisible(True)
            self.saveModeLabel.setVisible(True)
        else:
            self.saveModeBox.setEnabled(False)
            self.saveModeLabel.setEnabled(False)
            self.saveModeBox.setVisible(False)
            self.saveModeLabel.setVisible(False)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) # Required for all PyQt applications
    window = MainWindow()              # Instantiation of the MainWindow class
    window.show()                      # Paint the widgets onto the screen
    sys.exit(app.exec_())              # Start and exit the program cleanly
