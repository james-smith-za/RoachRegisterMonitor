import sys
from PyQt4 import QtGui, QtCore

import casperfpga

class RoachRegisterWidget(QtGui.QWidget):
    def __init__(self, register, regKey):
        super(RoachRegisterWidget, self).__init__()

        self.setLayout(QtGui.QHBoxLayout())

        self.label = QtGui.QLabel()
        self.label.setText("{0}:{1}".format(getattr(register, "name"), regKey))
        self.layout().addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setText("0")
        self.layout().addWidget(self.lineEdit)

        self.writeButton = QtGui.QPushButton()
        self.writeButton.setText("Write Register")
        self.layout().addWidget(self.writeButton)

        self.toggleButton = QtGui.QPushButton()
        self.toggleButton.setText("Toggle Register")
        self.layout().addWidget(self.toggleButton)

        self.pulseButton = QtGui.QPushButton()
        self.pulseButton.setText("Pulse register")
        self.layout().addWidget(self.pulseButton)

        self.register = register
        self.regKey = regKey

        QtCore.QObject.connect(self.writeButton, QtCore.SIGNAL("clicked()"), self.writeRegister)
        QtCore.QObject.connect(self.toggleButton, QtCore.SIGNAL("clicked()"), self.toggleRegister)
        QtCore.QObject.connect(self.pulseButton, QtCore.SIGNAL("clicked()"), self.pulseRegister)

        print "RoachRegisterWidget initialised."
        self.runTimer()

    def readRegister(self):
        registerValue = int(self.register.read()["data"][self.regKey])
        self.lineEdit.setText(str(registerValue))

    def writeRegister(self):
        dataToWrite = self.lineEdit.text()
        dataToWrite = "".join(c for c in setText if c.isdigit())
        writeArg = {self.regKey:int(dataToWrite)}
        self.register.write(**writeArg) # I love python :)

    def toggleRegister(self):
        writeArg = {self.regKey:"toggle"}
        self.register.write(**writeArg)

    def pulseRegister(self):
        writeArg = {self.regKey:"pulse"}
        self.register.write(**writeArg)

    def runTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.readRegister)
        self.timer.start(200)


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
        self.getFPGButton.setText("Get FPG file")
        self.layout().addWidget(self.getFPGButton)

        self.fpgName = QtGui.QLineEdit()
        self.fpgName.setText("None")
        self.layout().addWidget(self.fpgName)

        QtCore.QObject.connect(self.getFPGButton, QtCore.SIGNAL("clicked()"), self.getFPG)

        print "RoachLoaderWidget initialised."

    def getFPG(self):
        self.fpgFile = QtGui.QFileDialog.getOpenFileName(self, 'Open FPG file', '.')
        self.fpgName.setText(self.fpgFile)

