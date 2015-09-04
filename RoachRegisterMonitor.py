import sys
from PyQt4 import QtGui, QtCore
import casperfpga

class RoachRegisterMonitorWindow(QtGui.QWidget):
    def __init__(self):
        super(RoachRegisterMonitorWindow, self).__init__()

        self.initUI()

    def initUI(self):

        lblRoachName = QtGui.QLabel(self)
        lblRoachName.setText('Roach name or IP:')

        self.leRoachName = QtGui.QLineEdit(self)
        self.leRoachName.setText('catseye')

        btnGetFPG = QtGui.QPushButton('Choose FPG file', self)

        QtCore.QObject.connect(btnGetFPG, QtCore.SIGNAL('clicked()'), self.getFPG)

        roachNameHBox = QtGui.QHBoxLayout()
        roachNameHBox.addStretch(1)
        roachNameHBox.addWidget(lblRoachName)
        roachNameHBox.addWidget(self.leRoachName)
        roachNameHBox.addWidget(btnGetFPG)

        self.setLayout(roachNameHBox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('ROACH Register Monitor')
        self.show()

        self.runTimer()

    def getFPG(self):
        self.fpg_file = QtGui.QFileDialog.getOpenFileName(self, 'Open FPG file', '.')
        self.fpga = casperfpga.katcp_fpga.KatcpFpga(self.leRoachName.text)
        self.fpga.get_system_information(self.fpg_file)

        register_list = [reg for reg in dir(self.fpga.registers) if reg[0] != '_']

        self.registerList = [reg for reg in register_list if type(getattr(self.fpga.registers, reg)) == casperfpga.register.Register]

        self.registerWidgets = {}

        for reg in len(registerList):
            reg_name = getattr(reg, 'name')
            print regname




    #def updateRegisters(self):


    def runTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRegisters)
        self.timer.start(100)

def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = RoachRegisterMonitorWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


