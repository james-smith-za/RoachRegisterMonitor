import sys
from PyQt4 import QtGui, QtCore
import casperfpga


class RoachRegisterTrio(QtGui.QWidget):
    def __init__(self, register, regKey):
        super(RoachRegisterTrio, self).__init__()
        self.HorizLayout = QtGui.QHBoxLayout()
        self.HorizLayout.addStretch(1)

        self.label = QtGui.QLabel()
        self.label.setText("{0}:{1}".format(getattr(register, "name"), regKey))
        self.HorizLayout.addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setText("0")
        self.HorizLayout.addWidget(self.lineEdit)

        self.writeButton = QtGui.QPushButton()
        self.writeButton.setText("Write Register")
        self.HorizLayout.addWidget(self.writeButton)

        self.toggleButton = QtGui.QPushButton()
        self.toggleButton.setText("Toggle Register")
        self.HorizLayout.addWidget(self.toggleButton)

        self.pulseButton = QtGui.QPushButton()
        self.pulseButton.setText("Pulse register")
        self.HorizLayout.addWidget(self.pulseButton)

        self.register = register
        self.regKey = regKey

        QtCore.QObject.connect(self.writeButton, QtCore.SIGNAL("clicked()"), self.writeRegister)
        QtCore.QObject.connect(self.toggleButton, QtCore.SIGNAL("clicked()"), self.toggleRegister)
        QtCore.QObject.connect(self.pulseButton, QtCore.SIGNAL("clicked()"), self.pulseRegister)

        self.setGeometry(0, 0, 550, 30)
        print "Custom widget supposedly initialised..."
        #self.runTimer()

    def readRegister(self):
        registerValue = int(self.register.read()["data"][self.regKey])
        self.lineEdit.setText(str(registerValue))

    def writeRegister(self):
        dataToWrite = self.ui.lineEdit.text()
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



class RoachRegisterMonitorWindow(QtGui.QWidget):
    def __init__(self):
        super(RoachRegisterMonitorWindow, self).__init__()

        self.initUI()

    def initUI(self):

        lblRoachName = QtGui.QLabel(self)
        lblRoachName.setText('Roach name or IP:')

        self.leRoachName = QtGui.QLineEdit(self)
        self.leRoachName.setText('localhost')

        btnGetFPG = QtGui.QPushButton('Choose FPG file', self)

        #QtCore.QObject.connect(btnGetFPG, QtCore.SIGNAL('clicked()'), self.getFPG)

        roachNameHBox = QtGui.QHBoxLayout()
        roachNameHBox.addStretch(1)
        roachNameHBox.addWidget(lblRoachName)
        roachNameHBox.addWidget(self.leRoachName)
        roachNameHBox.addWidget(btnGetFPG)

        self.mainWindowVBox = QtGui.QVBoxLayout()
        self.mainWindowVBox.addStretch(1)
        self.mainWindowVBox.addLayout(roachNameHBox)

        #self.fpg_file = QtGui.QFileDialog.getOpenFileName(self, 'Open FPG file', '.')
        self.fpg_file = "nb_spectrometer_06_2015_Sep_07_1121.fpg"
        self.fpga = casperfpga.katcp_fpga.KatcpFpga('localhost')
        self.fpga.get_system_information(self.fpg_file)

        # List the names of the registers
        register_list = [reg for reg in dir(self.fpga.registers) if reg[0] != '_']

        # Get the actual register objects from the fpga object.
        self.registerList = [getattr(self.fpga.registers, reg) for reg in register_list if type(getattr(self.fpga.registers, reg)) == casperfpga.register.Register]

        self.widgetList = []

        for reg in self.registerList:
            regName = getattr(reg, 'name')
            regValue = reg.read()
            if regValue["data"].has_key("reg"):
                #print regName, regValue["data"]["reg"]
                newReg = RoachRegisterTrio(reg, "reg")
                self.widgetList.append(newReg)
                self.mainWindowVBox.addWidget(self.widgetList[-1])

            else:
                #print regName
                for key in regValue["data"].iterkeys():
                    #print key, regValue["data"][key]
                    newReg = RoachRegisterTrio(reg, key)
                    self.widgetList.append(newReg)
                    self.mainWindowVBox.addWidget(self.widgetList[-1])

        self.setLayout(self.mainWindowVBox)

        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('ROACH Register Monitor')
        self.show()

        #self.runTimer()


    def updateRegisters(self):
        print "Register updater called"


    def runTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRegisters)
        self.timer.start(1000)

def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = RoachRegisterMonitorWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


