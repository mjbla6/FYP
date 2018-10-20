# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'advancedlinemarkerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_advancedLineMarkerWindow(object):
    def setupUi(self, advancedLineMarkerWindow):
        advancedLineMarkerWindow.setObjectName("advancedLineMarkerWindow")
        advancedLineMarkerWindow.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(advancedLineMarkerWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelIntegLimit = QtWidgets.QLabel(advancedLineMarkerWindow)
        self.labelIntegLimit.setObjectName("labelIntegLimit")
        self.gridLayout.addWidget(self.labelIntegLimit, 2, 0, 1, 1)
        self.labelSweepLimit = QtWidgets.QLabel(advancedLineMarkerWindow)
        self.labelSweepLimit.setObjectName("labelSweepLimit")
        self.gridLayout.addWidget(self.labelSweepLimit, 0, 0, 1, 1)
        self.labelTraceInteg = QtWidgets.QLabel(advancedLineMarkerWindow)
        self.labelTraceInteg.setObjectName("labelTraceInteg")
        self.gridLayout.addWidget(self.labelTraceInteg, 3, 0, 1, 1)
        self.labelSearchLimit = QtWidgets.QLabel(advancedLineMarkerWindow)
        self.labelSearchLimit.setObjectName("labelSearchLimit")
        self.gridLayout.addWidget(self.labelSearchLimit, 1, 0, 1, 1)
        self.buttonSweepLimit = QtWidgets.QPushButton(advancedLineMarkerWindow)
        self.buttonSweepLimit.setCheckable(False)
        self.buttonSweepLimit.setObjectName("buttonSweepLimit")
        self.gridLayout.addWidget(self.buttonSweepLimit, 0, 1, 1, 1)
        self.buttonSrchLimit = QtWidgets.QPushButton(advancedLineMarkerWindow)
        self.buttonSrchLimit.setCheckable(False)
        self.buttonSrchLimit.setObjectName("buttonSrchLimit")
        self.gridLayout.addWidget(self.buttonSrchLimit, 1, 1, 1, 1)
        self.buttonIntegLimit = QtWidgets.QPushButton(advancedLineMarkerWindow)
        self.buttonIntegLimit.setCheckable(False)
        self.buttonIntegLimit.setObjectName("buttonIntegLimit")
        self.gridLayout.addWidget(self.buttonIntegLimit, 2, 1, 1, 1)
        self.buttonTraceInteg = QtWidgets.QPushButton(advancedLineMarkerWindow)
        self.buttonTraceInteg.setCheckable(False)
        self.buttonTraceInteg.setObjectName("buttonTraceInteg")
        self.gridLayout.addWidget(self.buttonTraceInteg, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(advancedLineMarkerWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(advancedLineMarkerWindow)
        self.buttonBox.accepted.connect(advancedLineMarkerWindow.accept)
        self.buttonBox.rejected.connect(advancedLineMarkerWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(advancedLineMarkerWindow)

    def retranslateUi(self, advancedLineMarkerWindow):
        _translate = QtCore.QCoreApplication.translate
        advancedLineMarkerWindow.setWindowTitle(_translate("advancedLineMarkerWindow", "Advanced Line Markers"))
        self.labelIntegLimit.setText(_translate("advancedLineMarkerWindow", "Integrate Limit"))
        self.labelSweepLimit.setText(_translate("advancedLineMarkerWindow", "Sweep Limit"))
        self.labelTraceInteg.setText(_translate("advancedLineMarkerWindow", "Trace Integration"))
        self.labelSearchLimit.setText(_translate("advancedLineMarkerWindow", "Search Limit"))
        self.buttonSweepLimit.setText(_translate("advancedLineMarkerWindow", "PushButton"))
        self.buttonSrchLimit.setText(_translate("advancedLineMarkerWindow", "PushButton"))
        self.buttonIntegLimit.setText(_translate("advancedLineMarkerWindow", "PushButton"))
        self.buttonTraceInteg.setText(_translate("advancedLineMarkerWindow", "PushButton"))

