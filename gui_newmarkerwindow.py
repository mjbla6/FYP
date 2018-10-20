# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newmarkerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_newMarkerWindow(object):
    def setupUi(self, newMarkerWindow):
        newMarkerWindow.setObjectName("newMarkerWindow")
        newMarkerWindow.resize(176, 187)
        self.verticalLayout = QtWidgets.QVBoxLayout(newMarkerWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelMkr = QtWidgets.QLabel(newMarkerWindow)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelMkr.setFont(font)
        self.labelMkr.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMkr.setObjectName("labelMkr")
        self.verticalLayout_2.addWidget(self.labelMkr)
        self.buttonMkrSel = QtWidgets.QPushButton(newMarkerWindow)
        self.buttonMkrSel.setObjectName("buttonMkrSel")
        self.verticalLayout_2.addWidget(self.buttonMkrSel)
        self.labelTrc = QtWidgets.QLabel(newMarkerWindow)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTrc.setFont(font)
        self.labelTrc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTrc.setObjectName("labelTrc")
        self.verticalLayout_2.addWidget(self.labelTrc)
        self.buttonTrcSel = QtWidgets.QPushButton(newMarkerWindow)
        self.buttonTrcSel.setObjectName("buttonTrcSel")
        self.verticalLayout_2.addWidget(self.buttonTrcSel)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(newMarkerWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(newMarkerWindow)
        self.buttonBox.accepted.connect(newMarkerWindow.accept)
        self.buttonBox.rejected.connect(newMarkerWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(newMarkerWindow)

    def retranslateUi(self, newMarkerWindow):
        _translate = QtCore.QCoreApplication.translate
        newMarkerWindow.setWindowTitle(_translate("newMarkerWindow", "New Marker"))
        self.labelMkr.setText(_translate("newMarkerWindow", "Marker:"))
        self.buttonMkrSel.setText(_translate("newMarkerWindow", "PushButton"))
        self.labelTrc.setText(_translate("newMarkerWindow", "Trace:"))
        self.buttonTrcSel.setText(_translate("newMarkerWindow", "PushButton"))

