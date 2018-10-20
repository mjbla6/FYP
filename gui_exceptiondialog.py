# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exceptiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_exceptionDialog(object):
    def setupUi(self, exceptionDialog):
        exceptionDialog.setObjectName("exceptionDialog")
        exceptionDialog.resize(400, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(exceptionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(exceptionDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(exceptionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(exceptionDialog)
        self.buttonBox.accepted.connect(exceptionDialog.accept)
        self.buttonBox.rejected.connect(exceptionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(exceptionDialog)

    def retranslateUi(self, exceptionDialog):
        _translate = QtCore.QCoreApplication.translate
        exceptionDialog.setWindowTitle(_translate("exceptionDialog", "Exception"))
        self.label.setText(_translate("exceptionDialog", "TextLabel"))

