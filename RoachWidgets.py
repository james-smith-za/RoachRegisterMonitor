import sys
from PyQt4 import QtGui, QtCore

import casperfpga

class RoachRegisterWidget(QtGui.QWidget):
    def __init__(self, register, regKey):
        super(RoachRegisterWidget, self).__init__()

        self.setLayout(QtGui.QHBoxLayout())

        self.label = QtGui.QLabel()
        self.regName = "{0}:{1}".format(getattr(register, "name"), regKey)
        self.label.setText(self.regName)
        self.layout().addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setText("0")
        self.layout().addWidget(self.lineEdit)

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
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("textEdited(QString)"), self.stopTimer)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("selectionChanged()"), self.stopTimer)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("returnPressed()"), self.writeRegister)

        self.timerLength = 200

        self.runTimer()

    def readRegister(self):
        registerValue = int(self.register.read()["data"][self.regKey])
        self.lineEdit.setText(str(registerValue))

    def writeRegister(self):
        dataToWrite = self.lineEdit.text()
        dataToWrite = "".join(c for c in str(self.lineEdit.text()) if c.isdigit())
        writeArg = {self.regKey:int(dataToWrite)}
        self.register.write(**writeArg) # I love python :)
        if not self.timer.isActive():
            self.runTimer()


    def toggleRegister(self):
        writeArg = {self.regKey:"toggle"}
        self.register.write(**writeArg)

    def pulseRegister(self):
        writeArg = {self.regKey:"pulse"}
        self.register.write(**writeArg)

    def runTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.readRegister)
        self.timer.start(self.timerLength)
        self.lineEdit.setStyleSheet("")

    def stopTimer(self):
        self.timer.stop()
        self.lineEdit.setStyleSheet("border: 1px solid red;")

    def filterWidget(self, filterString):
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
        self.fpgFile = QtGui.QFileDialog.getOpenFileName(self, 'Open FPG file', '.')
        self.fpgName.setText(self.fpgFile)


class RoachRegisterMonitor(QtGui.QWidget):
    def __init__(self):
        super(RoachRegisterMonitor, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        self.roachLoader = RoachLoaderWidget()
        self.layout().addWidget(self.roachLoader)

        self.connectButton = QtGui.QPushButton("Connect to ROACH", self)
        self.layout().addWidget(self.connectButton)

        self.filterLineEdit = QtGui.QLineEdit()
        self.filterLineEdit.setText("")
        self.filterLineEdit.setDisabled(True)
        self.layout().addWidget(self.filterLineEdit)

        QtCore.QObject.connect(self.connectButton, QtCore.SIGNAL("clicked()"), self.connectToRoach)
        QtCore.QObject.connect(self.filterLineEdit, QtCore.SIGNAL("textEdited(QString)"), self.filterList)

        self.widgetList = []

    def connectToRoach(self):
        self.fpga = casperfpga.katcp_fpga.KatcpFpga(str(self.roachLoader.lineEdit.text()))
        self.fpga.get_system_information(self.roachLoader.fpgFile)

        regNameList = [reg for reg in dir(self.fpga.registers) if reg[0] != '_']
        self.registerList = [getattr(self.fpga.registers, reg) for reg in regNameList if type(getattr(self.fpga.registers, reg)) == casperfpga.register.Register]


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

        self.filterLineEdit.setEnabled(True)

    def filterList(self):
        for widget in self.widgetList:
            widget.filterWidget(str(self.filterLineEdit.text()))




