from gui_hp8157a import Ui_HP8157A
from PyQt5 import QtCore, QtGui, QtWidgets
from __main__ import *

# Main class for the HP8157A machine
class hp8157A(QtWidgets.QWidget, Ui_HP8157A):
    def __init__(self, my_instrument2, parent=None):
        super(hp8157A, self).__init__(parent)
        self.setupUi(self)
        global instrument2
        instrument2 = my_instrument2
        att = instrument2.query("ATT?")
        self.spinBoxATT.setValue(float(att))
        cal = instrument2.query("CAL?")
        self.spinBoxCAL.setValue(float(cal))
        self.lcdAtt.display(float(att) + float(cal))
        wvl = instrument2.query("WVL?")
        wvl = float(wvl)
        wvl = wvl*(1000000000)
        wvl = int(wvl)
        self.spinBoxWL.setValue(wvl)
        D = instrument2.query("D?")
        D = int(D)
        if (D == 1):
            self.buttonDisable.setChecked(True)

        self.spinBoxATT.valueChanged.connect(self.valueChange)
        self.spinBoxCAL.valueChanged.connect(self.valueChange)
        self.spinBoxWL.valueChanged.connect(self.valueChange)
        self.buttonDisable.clicked.connect(self.unitEnable)

    def valueChange(self):
        self.lcdAtt.display(self.spinBoxATT.value() + self.spinBoxCAL.value())
        instrument2.write("WVL %i NM" % self.spinBoxWL.value())
        instrument2.write("CAL %f dB" % self.spinBoxCAL.value())
        instrument2.write("ATT %f dB" % self.spinBoxATT.value()) 

    def unitEnable(self):
        if self.buttonDisable.isChecked():
            instrument2.write("D1")
        else:
            instrument2.write("D0")
