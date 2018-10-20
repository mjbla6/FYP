# Remote Interface FYP 2018
# Mitch Blair & Isaac Naylor
#
# Last edit: 12/10/2018

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui_mainwindow import Ui_MainWindow
from gui_instrumentselect import Ui_instrumentSelect
from HP8157A import hp8157A
from AQ4303B import AQ4303B
import AGILENT86142B
import visa
import visa_manager

# VISA query to find available resources. Interacts with the visa_manager
# function to obtain information about the connected devices
rm = visa.ResourceManager()
resources =  rm.list_resources()
visa_details = visa_manager.returnVisa()
devices_info = visa_details[0]
address = visa_details[1]
num_devices = visa_details[2]

# Instrument select class adds in all available devices to the
# UI on start up and on click will start that machine process
class InstrumentSelect(QtWidgets.QDialog, Ui_instrumentSelect):
    def __init__(self, parent=None):
        super(InstrumentSelect, self).__init__(parent)
        self.setupUi(self)
        i = 0
        while i < num_devices:
            self.listWidget.addItem("%s" %devices_info[i])
            i += 1
        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)
        self.buttonRefresh.clicked.connect(self.refresh)

    # Refresh function will reload the devices connected. It works by reconnecting to the visa_manager module
    # which queries the GPIB connection and finds all connected devices. These are then added to the new
    # instrument window ready to connect
    def refresh(self):
        global devices_info
        global address
        global num_devices
        self.listWidget.clear()
        rm = visa.ResourceManager()
        resources =  rm.list_resources()
        visa_details = visa_manager.returnVisa()
        devices_info = visa_details[0]
        address = visa_details[1]
        num_devices = visa_details[2]
        i = 0
        while i < num_devices:
            self.listWidget.addItem("%s" %devices_info[i])
            i += 1
        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def onAccept(self):
        self.item = str(self.listWidget.currentItem())
        if self.item == 'None':
            self.selection = 0
            return self.selection
        else:
            self.selection = self.listWidget.currentItem().text()
            return self.selection

    def onReject(self):
        self.selection = ""
        return self.selection


# Main window
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.actionNew_Instrument.triggered.connect(self.instrumentSelectWindow)
        self.actionClose_Instrument.triggered.connect(self.closeTab)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

    def instrumentSelectWindow(self):
        widget = InstrumentSelect(parent=self)
        widget.exec_()
        if widget.selection != 0:
                self.openInstrument(widget.selection)

    # Once user selects an instrument in the Instrument Select, open the instrument in a new tab
    def openInstrument(self, device):
        if device == "AGILENT 86142B":
            global my_instrument
            ## TODO: why is there a flag here?
            ## should this be in the agilent code somewhere?
            global flag
            indice = [i for i, s in enumerate(devices_info) if 'AGILENT 86142B' in s]
            indice = indice[0]
            instrument_address = address[indice]
            my_instrument = rm.open_resource('%s' %instrument_address)
            self.tab = AGILENT86142B.Agilent86142B(my_instrument)
            flag = 1
        elif device == "HEWLETT PACKARD 8157A":
            global my_instrument2
            indice = [i for i, s in enumerate(devices_info) if 'HEWLETT PACKARD 8157A' in s]
            indice = indice[0]
            instrument_address = address[indice]
            my_instrument2 = rm.open_resource('%s' %instrument_address)
            self.tab = hp8157A(my_instrument2)
        elif device == "ANDO AQ-4303":
            global my_instrument3
            indice = [i for i, s in enumerate(devices_info) if 'ANDO AQ-4303' in s]
            indice = indice[0]
            instrument_address = address[indice]
            my_instrument3 = rm.open_resource('%s' %instrument_address)
            self.tab = AQ4303B(my_instrument3)
        elif device == "":
            return
        self.tabWidget.addTab(self.tab, "%s" %device)

    def closeTab(self, currentIndex):
        currentQWidget = self.tabWidget.widget(currentIndex)
        ##currentQWidget.deleteLater()
        self.tabWidget.removeTab(currentIndex)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
