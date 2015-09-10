#!/usr/bin/python
"""
RoachMonitor.py

This is the main script, it calls in the classes from the RoachWidgets module.
"""
import sys
from PyQt4 import QtGui, QtCore
from RoachWidgets import RoachRegisterWidget, RoachLoaderWidget, RoachRegisterMonitor

class myWindow(QtGui.QMainWindow):
    """Main window class to pull in all the others."""
    def __init__(self):
        """Initialise the class, set up a scrolling area in it."""
        super(myWindow, self).__init__()

        self.RRMWidget = RoachRegisterMonitor()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.RRMWidget)
        self.scrollArea.setWidgetResizable(True)

        self.setCentralWidget(self.scrollArea)

        # Possible future feature: some kind of dynamic resizing.
        # My mastery of PyQt isn't quite good enough for this yet though.
        self.setGeometry(300, 300, 600, 600)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())

