# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aq4303b.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AQ4303B(object):
    def setupUi(self, AQ4303B):
        AQ4303B.setObjectName("AQ4303B")
        AQ4303B.resize(800, 500)
        self.gridLayout_2 = QtWidgets.QGridLayout(AQ4303B)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LeftLayout = QtWidgets.QGridLayout()
        self.LeftLayout.setObjectName("LeftLayout")
        self.labelWL = QtWidgets.QLabel(AQ4303B)
        self.labelWL.setObjectName("labelWL")
        self.LeftLayout.addWidget(self.labelWL, 0, 0, 1, 1)
        self.labelLight = QtWidgets.QLabel(AQ4303B)
        self.labelLight.setObjectName("labelLight")
        self.LeftLayout.addWidget(self.labelLight, 0, 2, 1, 1)
        self.buttonWL = QtWidgets.QPushButton(AQ4303B)
        self.buttonWL.setObjectName("buttonWL")
        self.LeftLayout.addWidget(self.buttonWL, 0, 1, 1, 1)
        self.buttonLight = QtWidgets.QPushButton(AQ4303B)
        self.buttonLight.setObjectName("buttonLight")
        self.LeftLayout.addWidget(self.buttonLight, 0, 3, 1, 1)
        self.gridLayout_2.addLayout(self.LeftLayout, 0, 0, 1, 2)

        self.retranslateUi(AQ4303B)
        QtCore.QMetaObject.connectSlotsByName(AQ4303B)

    def retranslateUi(self, AQ4303B):
        _translate = QtCore.QCoreApplication.translate
        AQ4303B.setWindowTitle(_translate("AQ4303B", "Form"))
        self.labelWL.setText(_translate("AQ4303B", "WAVELENGTH (nm):"))
        self.labelLight.setText(_translate("AQ4303B", "LIGHT:"))
        self.buttonWL.setText(_translate("AQ4303B", "PushButton"))
        self.buttonLight.setText(_translate("AQ4303B", "PushButton"))

