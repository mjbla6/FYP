# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hp8157a.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HP8157A(object):
    def setupUi(self, HP8157A):
        HP8157A.setObjectName("HP8157A")
        HP8157A.resize(800, 500)
        self.gridLayout_2 = QtWidgets.QGridLayout(HP8157A)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LeftLayout = QtWidgets.QGridLayout()
        self.LeftLayout.setObjectName("LeftLayout")
        self.lcdAtt = QtWidgets.QLCDNumber(HP8157A)
        self.lcdAtt.setSmallDecimalPoint(False)
        self.lcdAtt.setObjectName("lcdAtt")
        self.LeftLayout.addWidget(self.lcdAtt, 0, 0, 1, 5)
        self.labelUnits = QtWidgets.QLabel(HP8157A)
        self.labelUnits.setObjectName("labelUnits")
        self.LeftLayout.addWidget(self.labelUnits, 0, 5, 1, 1)
        self.labelWL = QtWidgets.QLabel(HP8157A)
        self.labelWL.setObjectName("labelWL")
        self.LeftLayout.addWidget(self.labelWL, 1, 0, 1, 1)
        self.spinBoxWL = QtWidgets.QSpinBox(HP8157A)
        self.spinBoxWL.setMaximum(9999)
        self.spinBoxWL.setObjectName("spinBoxWL")
        self.LeftLayout.addWidget(self.spinBoxWL, 1, 1, 1, 1)
        self.labelCal = QtWidgets.QLabel(HP8157A)
        self.labelCal.setObjectName("labelCal")
        self.LeftLayout.addWidget(self.labelCal, 1, 2, 1, 1)
        self.spinBoxCAL = QtWidgets.QDoubleSpinBox(HP8157A)
        self.spinBoxCAL.setMinimum(-99.0)
        self.spinBoxCAL.setObjectName("spinBoxCAL")
        self.LeftLayout.addWidget(self.spinBoxCAL, 1, 3, 1, 1)
        self.labelAtt = QtWidgets.QLabel(HP8157A)
        self.labelAtt.setObjectName("labelAtt")
        self.LeftLayout.addWidget(self.labelAtt, 1, 4, 1, 1)
        self.spinBoxATT = QtWidgets.QDoubleSpinBox(HP8157A)
        self.spinBoxATT.setObjectName("spinBoxATT")
        self.LeftLayout.addWidget(self.spinBoxATT, 1, 5, 1, 1)
        self.gridLayout_2.addLayout(self.LeftLayout, 0, 0, 1, 2)
        self.buttonDisable = QtWidgets.QPushButton(HP8157A)
        self.buttonDisable.setCheckable(True)
        self.buttonDisable.setObjectName("buttonDisable")
        self.gridLayout_2.addWidget(self.buttonDisable, 2, 0, 1, 2)

        self.retranslateUi(HP8157A)
        QtCore.QMetaObject.connectSlotsByName(HP8157A)

    def retranslateUi(self, HP8157A):
        _translate = QtCore.QCoreApplication.translate
        HP8157A.setWindowTitle(_translate("HP8157A", "Form"))
        self.labelUnits.setText(_translate("HP8157A", "dB"))
        self.labelWL.setText(_translate("HP8157A", "WAVELENGTH:"))
        self.labelCal.setText(_translate("HP8157A", "CAL:"))
        self.labelAtt.setText(_translate("HP8157A", "ATT:"))
        self.buttonDisable.setText(_translate("HP8157A", "Disable"))

