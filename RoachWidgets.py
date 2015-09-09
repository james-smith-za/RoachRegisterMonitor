#/usr/bin/python
"""
RoachWidgets.py

File contains definitions of compount widgets written to make accessing the registers
on a ROACH board easier.
Can probably be expanded to actually program the ROACH, but this invariably involves
a slightly more complex script to initialise registers and sync things up, so that's
probably best left for the scripts we're used to. This is just a nice tool to keep an
eye on things.

Author: J. Smith (jsmith@ska.ac.za)
"""
import sys
from PyQt4 import QtGui, QtCore

import casperfpga

class RoachRegisterWidget(QtGui.QWidget):
    """Qt Widget describing a register on the ROACH.

    Contains a label with the register's name, a line-edit with its value which
    is updated periodically and can be edited by the user, and buttons to write
    the desired value, or alternately to toggle or pulse (more useful in the case
    of single-bit register fields).
    """
    def __init__(self, register, regKey):
        super(RoachRegisterWidget, self).__init__()

        self.setLayout(QtGui.QHBoxLayout())

        self.label = QtGui.QLabel()
        self.regName = "{0}:{1}".format(getattr(register, "name"), regKey)
        self.label.setText(self.regName)
        self.layout().addWidget(self.label)

        self.spinBox = QtGui.QSpinBox()
        self.spinBox.setValue(0)
        self.spinBox.setMaximum(2**32)
        self.spinBox.setMinimum(0)
        self.layout().addWidget(self.spinBox)

        self.writeButton = QtGui.QPushButton()
        self.writeButton.setText("Write")
        self.layout().addWidget(self.writeButton)

        self.toggleButton = QtGui.QPushButton()
        self.toggleButton.setText("Toggle")
        self.layout().addWidget(self.toggleButton)

        self.pulseButton = QtGui.QPushButton()
        self.pulseButton.setText("Pulse")
        self.layout().addWidget(self.pulseButton)

        self.register = register
        self.regKey = regKey

        QtCore.QObject.connect(self.writeButton, QtCore.SIGNAL("clicked()"), self.writeRegister)
        QtCore.QObject.connect(self.toggleButton, QtCore.SIGNAL("clicked()"), self.toggleRegister)
        QtCore.QObject.connect(self.pulseButton, QtCore.SIGNAL("clicked()"), self.pulseRegister)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.writeRegister)

        self.timerLength = 200

        self.runTimer()

    def readRegister(self):
        """Read the value from the register and set the line edit's text."""
        registerValue = int(self.register.read()["data"][self.regKey])
        self.spinBox.setValue(int(registerValue))

    def writeRegister(self):
        """Write the line edit's text to the corresponding register."""
        dataToWrite = int(self.spinBox.value())
        writeArg = {self.regKey:dataToWrite}
        self.register.write(**writeArg) # I love python :)
        if not self.timer.isActive():
            self.runTimer()

    def toggleRegister(self):
        """Toggle the register's value."""
        writeArg = {self.regKey:"toggle"}
        self.register.write(**writeArg)

    def pulseRegister(self):
        """Write a pulse to the register."""
        writeArg = {self.regKey:"pulse"}
        self.register.write(**writeArg)

    def runTimer(self):
        """Start the timer for polling the register. Also set the line edit to look default."""
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.readRegister)
        self.timer.start(self.timerLength)

    def stopTimer(self):
        """Stop the timer for polling the register. Highlight the line edit to indicate data not yet written."""
        self.timer.stop()

    def filterWidget(self, filterString):
        """Decide whether to show or hide the register based on the given filter string."""
        if str(filterString) in str(self.regName):
            self.setEnabled(True)
            self.setVisible(True)
            self.timer.start(self.timerLength)
        elif filterString == "":
            self.setEnabled(True)
            self.setVisible(True)
            self.timer.start(self.timerLength)
        else:
            self.setEnabled(False)
            self.setVisible(False)
            self.timer.stop()

class RoachLoaderWidget(QtGui.QWidget):
    """Widget to connect to the ROACH and load up the required .fpg file in order to be able to communicate."""
    def __init__(self):
        super(RoachLoaderWidget, self).__init__()

        self.setLayout(QtGui.QHBoxLayout())

        self.label = QtGui.QLabel()
        self.label.setText("Roach hostname or IP:")
        self.layout().addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setText("localhost")
        self.layout().addWidget(self.lineEdit)

        self.getFPGButton = QtGui.QPushButton()
        self.getFPGButton.setText("Browse (for FPG)")
        self.layout().addWidget(self.getFPGButton)

        self.fpgName = QtGui.QLineEdit()
        self.fpgName.setText("None")
        self.layout().addWidget(self.fpgName)

        QtCore.QObject.connect(self.getFPGButton, QtCore.SIGNAL("clicked()"), self.getFPG)

    def getFPG(self):
        """Bring up a browse window to find the .fpg file."""
        self.fpgFile = QtGui.QFileDialog.getOpenFileName(self, 'Open FPG file', '.')
        self.fpgName.setText(self.fpgFile)

class RoachRegisterMonitor(QtGui.QWidget):
    """Widget to encapsulate the other two.

    This widget will have a RoachLoaderWidget at the top, and it will populate its widget list with
    as many RoachRegisterMonitor widgets as it needs to handle the FPG file.
    """
    def __init__(self):
        super(RoachRegisterMonitor, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        self.roachLoader = RoachLoaderWidget()
        self.layout().addWidget(self.roachLoader)

        self.connectButton = QtGui.QPushButton("Connect to ROACH", self)
        self.layout().addWidget(self.connectButton)

        self.filterLineEdit = QtGui.QLineEdit()
        self.filterLineEdit.setText("ROACH not yet connected...")
        self.filterLineEdit.setDisabled(True)
        self.layout().addWidget(self.filterLineEdit)

        QtCore.QObject.connect(self.connectButton, QtCore.SIGNAL("clicked()"), self.connectToRoach)
        QtCore.QObject.connect(self.filterLineEdit, QtCore.SIGNAL("textEdited(QString)"), self.filterList)

        self.widgetList = []

    def connectToRoach(self):
        """Connect to the ROACH and read all its register information."""
        self.filterLineEdit.setEnabled(True)
        self.filterLineEdit.setText("Type here to filter registers by name")

        self.fpga = casperfpga.katcp_fpga.KatcpFpga(str(self.roachLoader.lineEdit.text()))
        self.fpga.get_system_information(self.roachLoader.fpgFile)

        # Not interested in the registers with names beginning in '_'
        regNameList = [reg for reg in dir(self.fpga.registers) if reg[0] != '_']
        # Not everything that fpga.registers has in it is actually a readable / writeable register
        # for some reason, so we just remove the ones we don't want.
        self.registerList = [getattr(self.fpga.registers, reg) for reg in regNameList if type(getattr(self.fpga.registers, reg)) == casperfpga.register.Register]

        # casperfpga returns the register values in a dictionary - if it's a single value, the key
        # name is "reg", otherwise we can handle each individual data item separately.
        for reg in self.registerList:
            regValue = reg.read()
            if regValue["data"].has_key("reg"):
                newReg = RoachRegisterWidget(reg, "reg")
                self.widgetList.append(newReg)
                self.layout().addWidget(self.widgetList[-1])
            else:
                for key in regValue["data"].iterkeys():
                    newReg = RoachRegisterWidget(reg, key)
                    self.widgetList.append(newReg)
                    self.layout().addWidget(self.widgetList[-1])

    def filterList(self):
        """When the text in the filter box changes, run through the widget list and let each widget filter itself."""
        for widget in self.widgetList:
            widget.filterWidget(str(self.filterLineEdit.text()))

if __name__ == "__main__":
    pass

