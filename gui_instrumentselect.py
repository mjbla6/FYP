# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instrumentselect.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_instrumentSelect(object):
    def setupUi(self, instrumentSelect):
        instrumentSelect.setObjectName("instrumentSelect")
        instrumentSelect.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(instrumentSelect)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(instrumentSelect)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.buttonRefresh = QtWidgets.QPushButton(instrumentSelect)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.gridLayout.addWidget(self.buttonRefresh, 1, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(instrumentSelect)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 2)

        self.retranslateUi(instrumentSelect)
        self.buttonBox.accepted.connect(instrumentSelect.accept)
        self.buttonBox.rejected.connect(instrumentSelect.reject)
        QtCore.QMetaObject.connectSlotsByName(instrumentSelect)

    def retranslateUi(self, instrumentSelect):
        _translate = QtCore.QCoreApplication.translate
        instrumentSelect.setWindowTitle(_translate("instrumentSelect", "New Instrument"))
        self.buttonRefresh.setText(_translate("instrumentSelect", "Refresh"))

