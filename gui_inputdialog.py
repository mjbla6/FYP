# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_inputDialog(object):
    def setupUi(self, inputDialog):
        inputDialog.setObjectName("inputDialog")
        inputDialog.resize(400, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(inputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(inputDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label = QtWidgets.QLabel(inputDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(inputDialog)
        self.buttonBox.accepted.connect(inputDialog.accept)
        self.buttonBox.rejected.connect(inputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(inputDialog)

    def retranslateUi(self, inputDialog):
        _translate = QtCore.QCoreApplication.translate
        inputDialog.setWindowTitle(_translate("inputDialog", "Dialog"))
        self.label.setText(_translate("inputDialog", "TextLabel"))

