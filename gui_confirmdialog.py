# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_confirmDialog(object):
    def setupUi(self, confirmDialog):
        confirmDialog.setObjectName("confirmDialog")
        confirmDialog.resize(400, 82)
        self.verticalLayout = QtWidgets.QVBoxLayout(confirmDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(confirmDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(confirmDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(confirmDialog)
        self.buttonBox.accepted.connect(confirmDialog.accept)
        self.buttonBox.rejected.connect(confirmDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(confirmDialog)

    def retranslateUi(self, confirmDialog):
        _translate = QtCore.QCoreApplication.translate
        confirmDialog.setWindowTitle(_translate("confirmDialog", "Confirm"))
        self.label.setText(_translate("confirmDialog", "Are you sure?"))

