# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 900, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew_Instrument = QtWidgets.QAction(MainWindow)
        self.actionNew_Instrument.setObjectName("actionNew_Instrument")
        self.actionClose_Instrument = QtWidgets.QAction(MainWindow)
        self.actionClose_Instrument.setObjectName("actionClose_Instrument")
        self.menu_File.addAction(self.actionNew_Instrument)
        self.menu_File.addAction(self.actionClose_Instrument)
        self.menu_File.addSeparator()
        self.menuBar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Virtual Lab"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.actionNew_Instrument.setText(_translate("MainWindow", "New Instrument"))
        self.actionNew_Instrument.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionClose_Instrument.setText(_translate("MainWindow", "Close Instrument"))
        self.actionClose_Instrument.setShortcut(_translate("MainWindow", "Ctrl+W"))

