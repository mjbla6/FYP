# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'markersetupwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_markerSetupWindow(object):
    def setupUi(self, markerSetupWindow):
        markerSetupWindow.setObjectName("markerSetupWindow")
        markerSetupWindow.resize(500, 423)
        self.verticalLayout = QtWidgets.QVBoxLayout(markerSetupWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.buttonUserMkrThresh = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonUserMkrThresh.setObjectName("buttonUserMkrThresh")
        self.gridLayout.addWidget(self.buttonUserMkrThresh, 6, 4, 1, 2)
        self.label = QtWidgets.QLabel(markerSetupWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(markerSetupWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 4)
        self.label_12 = QtWidgets.QLabel(markerSetupWindow)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 7, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(markerSetupWindow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 4)
        self.label_4 = QtWidgets.QLabel(markerSetupWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 4)
        self.label_5 = QtWidgets.QLabel(markerSetupWindow)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 4)
        self.buttonBWMkrInterp = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonBWMkrInterp.setObjectName("buttonBWMkrInterp")
        self.gridLayout.addWidget(self.buttonBWMkrInterp, 4, 4, 1, 2)
        self.buttonMkrInterp = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonMkrInterp.setObjectName("buttonMkrInterp")
        self.gridLayout.addWidget(self.buttonMkrInterp, 3, 4, 1, 2)
        self.linePitExcur = QtWidgets.QLineEdit(markerSetupWindow)
        self.linePitExcur.setObjectName("linePitExcur")
        self.gridLayout.addWidget(self.linePitExcur, 5, 4, 1, 1)
        self.buttonDeltaMkrUnits = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonDeltaMkrUnits.setObjectName("buttonDeltaMkrUnits")
        self.gridLayout.addWidget(self.buttonDeltaMkrUnits, 2, 4, 1, 2)
        self.buttonNormMkrUnits = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonNormMkrUnits.setCheckable(False)
        self.buttonNormMkrUnits.setObjectName("buttonNormMkrUnits")
        self.gridLayout.addWidget(self.buttonNormMkrUnits, 0, 4, 1, 2)
        self.buttonBWMkrUnits = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonBWMkrUnits.setCheckable(False)
        self.buttonBWMkrUnits.setObjectName("buttonBWMkrUnits")
        self.gridLayout.addWidget(self.buttonBWMkrUnits, 1, 4, 1, 2)
        self.lineOSNR = QtWidgets.QLineEdit(markerSetupWindow)
        self.lineOSNR.setObjectName("lineOSNR")
        self.gridLayout.addWidget(self.lineOSNR, 9, 4, 1, 1)
        self.label_16 = QtWidgets.QLabel(markerSetupWindow)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 9, 5, 1, 1)
        self.linePeakExcur = QtWidgets.QLineEdit(markerSetupWindow)
        self.linePeakExcur.setObjectName("linePeakExcur")
        self.gridLayout.addWidget(self.linePeakExcur, 5, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(markerSetupWindow)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(markerSetupWindow)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 5, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(markerSetupWindow)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(markerSetupWindow)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(markerSetupWindow)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 7, 0, 1, 4)
        self.lineSrchThresh = QtWidgets.QLineEdit(markerSetupWindow)
        self.lineSrchThresh.setObjectName("lineSrchThresh")
        self.gridLayout.addWidget(self.lineSrchThresh, 7, 4, 1, 1)
        self.buttonNoiseMkrBW = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonNoiseMkrBW.setObjectName("buttonNoiseMkrBW")
        self.gridLayout.addWidget(self.buttonNoiseMkrBW, 8, 4, 1, 2)
        self.label_15 = QtWidgets.QLabel(markerSetupWindow)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 9, 0, 1, 2)
        self.label_13 = QtWidgets.QLabel(markerSetupWindow)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 8, 0, 1, 4)
        self.buttonOSNR = QtWidgets.QPushButton(markerSetupWindow)
        self.buttonOSNR.setObjectName("buttonOSNR")
        self.gridLayout.addWidget(self.buttonOSNR, 9, 2, 1, 2)
        self.label_10 = QtWidgets.QLabel(markerSetupWindow)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 6, 0, 1, 4)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(markerSetupWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(markerSetupWindow)
        self.buttonBox.accepted.connect(markerSetupWindow.accept)
        self.buttonBox.rejected.connect(markerSetupWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(markerSetupWindow)

    def retranslateUi(self, markerSetupWindow):
        _translate = QtCore.QCoreApplication.translate
        markerSetupWindow.setWindowTitle(_translate("markerSetupWindow", "Markers Setup"))
        self.buttonUserMkrThresh.setText(_translate("markerSetupWindow", "PushButton"))
        self.label.setText(_translate("markerSetupWindow", "Normal Marker Units:"))
        self.label_2.setText(_translate("markerSetupWindow", "BW Marker Units:"))
        self.label_12.setText(_translate("markerSetupWindow", "dBm"))
        self.label_3.setText(_translate("markerSetupWindow", "Delta Marker Units:"))
        self.label_4.setText(_translate("markerSetupWindow", "Normal/Delta Marker Interpolation:"))
        self.label_5.setText(_translate("markerSetupWindow", "Bandwidth Marker Interpolation:"))
        self.buttonBWMkrInterp.setText(_translate("markerSetupWindow", "PushButton"))
        self.buttonMkrInterp.setText(_translate("markerSetupWindow", "PushButton"))
        self.buttonDeltaMkrUnits.setText(_translate("markerSetupWindow", "PushButton"))
        self.buttonNormMkrUnits.setText(_translate("markerSetupWindow", "PushButton"))
        self.buttonBWMkrUnits.setText(_translate("markerSetupWindow", "PushButton"))
        self.label_16.setText(_translate("markerSetupWindow", "nm"))
        self.label_9.setText(_translate("markerSetupWindow", "Pit Excursion:"))
        self.label_8.setText(_translate("markerSetupWindow", "dB"))
        self.label_6.setText(_translate("markerSetupWindow", "Peak Excursion:"))
        self.label_7.setText(_translate("markerSetupWindow", "dB"))
        self.label_11.setText(_translate("markerSetupWindow", "Marker Search Threshold Value:"))
        self.buttonNoiseMkrBW.setText(_translate("markerSetupWindow", "PushButton"))
        self.label_15.setText(_translate("markerSetupWindow", "OSNR Noise:"))
        self.label_13.setText(_translate("markerSetupWindow", "Noise Marker Reference Bandwidth:"))
        self.buttonOSNR.setText(_translate("markerSetupWindow", "PushButton"))
        self.label_10.setText(_translate("markerSetupWindow", "User Marker Search Threshold:"))