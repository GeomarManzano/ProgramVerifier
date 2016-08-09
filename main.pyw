#! /usr/bin/python

# Author: Geomar Manzano

import sys           # used for a clean exit of the application
import subprocess    # to run external programs
import ntpath        # to parse paths
import difflib       # to show differences between files
import textDialog    # text dialog in order to show differences
from PyQt4 import QtCore, QtGui

TIMER = 3000 # 3000 milliseconds is equal to 3 seconds

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Instance variables
        self.progPath = None
        self.testFilePath = None
        
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
        self.progLabel = QtGui.QLabel('&Program')
        self.inputTestLabel = QtGui.QLabel('&Test File')
        self.progButton = QtGui.QPushButton('Browse')
        self.inputTestButton = QtGui.QPushButton('Browse')
        self.runButton = QtGui.QPushButton('&Run')
        self.loadedProg = QtGui.QLineEdit()
        self.loadedTestFile = QtGui.QLineEdit()
        self.saveModeLabel = QtGui.QLabel('&Save Mode')
        self.saveModeBox = QtGui.QComboBox()
        self.saveModeBox.addItems(['Overwrite', 'Append'])
        
        # Dialogs
        self.errDlg = QtGui.QMessageBox(self)
        self.infoDlg = QtGui.QMessageBox(self)
        
        # Buddies
        self.progLabel.setBuddy(self.progButton)
        self.inputTestLabel.setBuddy(self.inputTestButton)
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

        # Output mode is a submenu of Options with On Screen and Text File
        # as options for it
        self.outputMenu = self.optionMenu.addMenu('Output Mode')
        self.outputMenu.addAction(self.onScreen_action)
        self.outputMenu.addAction(self.offScreen_action)
    def programOpen_slot(self):
        self.progPath = QtGui.QFileDialog.getOpenFileName(self, 'Open Program')

        # If the user did not cancel the file dialog
        if not self.progPath.isEmpty() and not self.progPath.isNull():
            self.status.showMessage('Program loaded', TIMER)
            progHead, self.progTail = ntpath.split(str(self.progPath))
            self.loadedProg.setText(self.progTail)
        else:
            self.loadedProg.clear() # User canceled the file dialog
    def fileOpen_slot(self):
        self.testFilePath = QtGui.QFileDialog.getOpenFileName(self, 'Open File')

        # If the user did not cancel the file dialog
        if not self.testFilePath.isEmpty() and not self.testFilePath.isNull():
            self.status.showMessage('File loaded', TIMER)
            fileHead, self.fileTail = ntpath.split(str(self.testFilePath))
            self.loadedTestFile.setText(self.fileTail)
        else:
            self.loadedTestFile.clear() # User canceled the file dialog
    def execProgram_slot(self):
        try:
            process = subprocess.Popen(
                [str(self.progPath)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            # Get the output and error code of the given program
            output, err = process.communicate()
            process.wait()
            output_lines = output.strip().splitlines()

            # Open the test file and read its content
            with open(str(self.testFilePath)) as testFile:
                testFile_lines = testFile.read().splitlines()

            self.status.showMessage('Program Executed', TIMER)
            
            # Output a message box if the program output and the given text
            # file are the same and immediately return so nothing else is
            # done
            if output_lines == testFile_lines:
                self.infoDlg.information(
                    self, 'Info', 'Program output and text file are the same')
                return

            diff = '\n'.join(list(
                difflib.unified_diff(output_lines, testFile_lines,
                                     fromfile=self.progTail,
                                     tofile=self.fileTail,
                                     lineterm='')))
            diff += '\n\n'

            if self.onScreen_action.isChecked():
                # Note: replacing self.dlg with dlg will possibly cause dlg
                # to be garbage collected once this method is done executing.
                # Therefore it's required to add the self in to keep the
                # dialog in scope
                self.dlg = textDialog.TextDialog(self.progTail + ' output',
                                                 diff)

                # Modeless dialog showing differences of the program output
                # and the given text file
                self.dlg.show()
            elif self.offScreen_action.isChecked():
                openedFile = open(self.saveFile, self.mode)

                # Write the differences between the program output and the given
                # text file in the specified save file
                openedFile.write(diff)
                openedFile.close()
        except OSError:
            self.errDlg.critical(self, 'Error', 'No program entered')
        except IOError:
            self.errDlg.critical(self, 'Error', 'No test file entered')
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
        self.progButton.clicked.connect(self.programOpen_slot)
        self.inputTestButton.clicked.connect(self.fileOpen_slot)
        self.runButton.clicked.connect(self.execProgram_slot)
        self.saveModeBox.currentIndexChanged.connect(self.setSaveMode_slot)
    def initUI(self):
        # The text fields for the loaded program and the loaded test file are
        # set to disabled since they are only used for showing information
        self.loadedProg.setEnabled(False)
        self.loadedTestFile.setEnabled(False)

        # We initially hide the options for the save mode since they are only
        # reserved for the Output Text File option
        self.saveMode(False)
        
        # Central Widget layout setup
        layout = QtGui.QGridLayout()
        layout.addWidget(self.progLabel, 0, 0)
        layout.addWidget(self.progButton, 0, 2)
        layout.addWidget(self.loadedProg, 0, 1)
        layout.addWidget(self.inputTestLabel, 2, 0)
        layout.addWidget(self.inputTestButton, 2, 2)
        layout.addWidget(self.loadedTestFile, 2, 1)
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
    app = QtGui.QApplication([])       # Required for all PyQt applications
    window = MainWindow()              # Instantiation of the MainWindow class
    window.show()                      # Paint the widgets onto the screen
    sys.exit(app.exec_())              # Start and exit the program cleanly
