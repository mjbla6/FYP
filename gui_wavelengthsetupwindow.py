# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wavelengthsetupwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wavelengthSetupWindow(object):
    def setupUi(self, wavelengthSetupWindow):
        wavelengthSetupWindow.setObjectName("wavelengthSetupWindow")
        wavelengthSetupWindow.resize(400, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(wavelengthSetupWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(wavelengthSetupWindow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(wavelengthSetupWindow)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.lineWLOffset = QtWidgets.QLineEdit(wavelengthSetupWindow)
        self.lineWLOffset.setObjectName("lineWLOffset")
        self.gridLayout.addWidget(self.lineWLOffset, 1, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(wavelengthSetupWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(wavelengthSetupWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineWLStep = QtWidgets.QLineEdit(wavelengthSetupWindow)
        self.lineWLStep.setObjectName("lineWLStep")
        self.gridLayout.addWidget(self.lineWLStep, 2, 1, 1, 2)
        self.buttonWLRef = QtWidgets.QPushButton(wavelengthSetupWindow)
        self.buttonWLRef.setObjectName("buttonWLRef")
        self.gridLayout.addWidget(self.buttonWLRef, 3, 2, 1, 2)
        self.buttonWLUnits = QtWidgets.QPushButton(wavelengthSetupWindow)
        self.buttonWLUnits.setObjectName("buttonWLUnits")
        self.gridLayout.addWidget(self.buttonWLUnits, 0, 2, 1, 2)
        self.label = QtWidgets.QLabel(wavelengthSetupWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(wavelengthSetupWindow)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(wavelengthSetupWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(wavelengthSetupWindow)
        self.buttonBox.accepted.connect(wavelengthSetupWindow.accept)
        self.buttonBox.rejected.connect(wavelengthSetupWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(wavelengthSetupWindow)

    def retranslateUi(self, wavelengthSetupWindow):
        _translate = QtCore.QCoreApplication.translate
        wavelengthSetupWindow.setWindowTitle(_translate("wavelengthSetupWindow", "Wavelength Setup"))
        self.label_3.setText(_translate("wavelengthSetupWindow", "nm"))
        self.label_5.setText(_translate("wavelengthSetupWindow", "nm"))
        self.label_4.setText(_translate("wavelengthSetupWindow", "Center Wavelength Step Size:"))
        self.label_2.setText(_translate("wavelengthSetupWindow", "Wavelength Offset:"))
        self.buttonWLRef.setText(_translate("wavelengthSetupWindow", "PushButton"))
        self.buttonWLUnits.setText(_translate("wavelengthSetupWindow", "PushButton"))
        self.label.setText(_translate("wavelengthSetupWindow", "Wavelength Units:"))
        self.label_6.setText(_translate("wavelengthSetupWindow", "Wavelengths Referenced In:"))

