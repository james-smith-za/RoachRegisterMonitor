import sys
from PyQt4 import QtGui, QtCore

from RoachWidgets import RoachRegisterWidget, RoachLoaderWidget

import casperfpga

class RoachRegisterMonitor(QtGui.QWidget):
    def __init__(self):
        super(RoachRegisterMonitor, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        self.roachLoader = RoachLoaderWidget()
        self.layout().addWidget(self.roachLoader)

        self.connectButton = QtGui.QPushButton("Connect to ROACH", self)
        self.layout().addWidget(self.connectButton)

        QtCore.QObject.connect(self.connectButton, QtCore.SIGNAL("clicked()"), self.connectToRoach)

    def connectToRoach(self):
        self.fpga = casperfpga.katcp_fpga.KatcpFpga(str(self.roachLoader.lineEdit.text()))
        self.fpga.get_system_information(self.roachLoader.fpgFile)

        regNameList = [reg for reg in dir(self.fpga.registers) if reg[0] != '_']
        self.registerList = [getattr(self.fpga.registers, reg) for reg in regNameList if type(getattr(self.fpga.registers, reg)) == casperfpga.register.Register]

        self.widgetList = []

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





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = RoachRegisterMonitor()
    myWindow.show()
    sys.exit(app.exec_())


