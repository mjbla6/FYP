# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activemarkerswindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_activeMarkersWindow(object):
    def setupUi(self, activeMarkersWindow):
        activeMarkersWindow.setObjectName("activeMarkersWindow")
        activeMarkersWindow.resize(176, 185)
        self.verticalLayout = QtWidgets.QVBoxLayout(activeMarkersWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkMkr1 = QtWidgets.QCheckBox(activeMarkersWindow)
        self.checkMkr1.setObjectName("checkMkr1")
        self.verticalLayout_2.addWidget(self.checkMkr1)
        self.checkMkr2 = QtWidgets.QCheckBox(activeMarkersWindow)
        self.checkMkr2.setObjectName("checkMkr2")
        self.verticalLayout_2.addWidget(self.checkMkr2)
        self.checkMkr3 = QtWidgets.QCheckBox(activeMarkersWindow)
        self.checkMkr3.setObjectName("checkMkr3")
        self.verticalLayout_2.addWidget(self.checkMkr3)
        self.checkMkr4 = QtWidgets.QCheckBox(activeMarkersWindow)
        self.checkMkr4.setObjectName("checkMkr4")
        self.verticalLayout_2.addWidget(self.checkMkr4)
        self.buttonAllOff = QtWidgets.QPushButton(activeMarkersWindow)
        self.buttonAllOff.setObjectName("buttonAllOff")
        self.verticalLayout_2.addWidget(self.buttonAllOff)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(activeMarkersWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(activeMarkersWindow)
        self.buttonBox.accepted.connect(activeMarkersWindow.accept)
        self.buttonBox.rejected.connect(activeMarkersWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(activeMarkersWindow)

    def retranslateUi(self, activeMarkersWindow):
        _translate = QtCore.QCoreApplication.translate
        activeMarkersWindow.setWindowTitle(_translate("activeMarkersWindow", "Displayed Markers"))
        self.checkMkr1.setText(_translate("activeMarkersWindow", "Mkr 1"))
        self.checkMkr2.setText(_translate("activeMarkersWindow", "Mkr 2"))
        self.checkMkr3.setText(_translate("activeMarkersWindow", "Mkr 3"))
        self.checkMkr4.setText(_translate("activeMarkersWindow", "Mkr 4"))
        self.buttonAllOff.setText(_translate("activeMarkersWindow", "All Off"))

