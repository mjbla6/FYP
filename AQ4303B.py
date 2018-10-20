from gui_aq4303b import Ui_AQ4303B
from PyQt5 import QtCore, QtGui, QtWidgets
from __main__ import *

# Main class for the AQ4303B machine
class AQ4303B(QtWidgets.QWidget, Ui_AQ4303B):
    def __init__(self, my_instrument3, parent=None):
        super(AQ4303B, self).__init__(parent)
        self.setupUi(self)
        global instrument3
        instrument3 = my_instrument3
        instrument3.write("B")
        instrument3.write("C")
        light = '270Hz'
        wavelength = '400-600'
        self.buttonWL.setText(wavelength)
        self.buttonLight.setText(light)

        self.WL = QtWidgets.QMenu()
        self.WL.addAction("400-600", self.WLAction1)
        self.WL.addAction("600-1000", self.WLAction2)
        self.WL.addAction("1000-1800", self.WLAction3)
        self.buttonWL.setMenu(self.WL)

        self.lightMenu = QtWidgets.QMenu()
        self.lightMenu.addAction("CW", self.lightMenuAction1)
        self.lightMenu.addAction("270Hz", self.lightMenuAction2)
        self.buttonLight.setMenu(self.lightMenu)

    def lightMenuAction1(self):
        self.buttonLight.setText("CW")
        instrument3.write("A")

    def lightMenuAction2(self):
        self.buttonLight.setText("270Hz")
        instrument3.write("B")

    def WLAction1(self):
        self.buttonWL.setText("400-600")
        instrument3.write("C")

    def WLAction2(self):
        self.buttonWL.setText("600-1000")
        instrument3.write("D")

    def WLAction3(self):
        self.buttonWL.setText("1000-1800")
        instrument3.write("E")
