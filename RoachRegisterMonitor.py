import sys
from PyQt4 import QtGui, QtCore

from RoachWidgets import RoachRegisterWidget, RoachLoaderWidget, RoachRegisterMonitor

import casperfpga

class myWindow(QtGui.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()

        self.RRMWidget = RoachRegisterMonitor()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.RRMWidget)
        self.scrollArea.setWidgetResizable(True)

        self.setCentralWidget(self.scrollArea)

        self.setGeometry(300, 300, 600, 600)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())


