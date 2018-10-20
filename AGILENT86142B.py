from PyQt5 import QtCore, QtGui, QtWidgets
from gui_inputdialog import Ui_inputDialog
from gui_exceptiondialog import Ui_exceptionDialog
from gui_confirmdialog import Ui_confirmDialog
from gui_agilent86142b import Ui_Agilent86142B
from gui_amplitudesetupwindow import Ui_amplitudeSetupWindow
from gui_wavelengthsetupwindow import Ui_wavelengthSetupWindow
from gui_activemarkerswindow import Ui_activeMarkersWindow
from gui_markersetupwindow import Ui_markerSetupWindow
from gui_advancedlinemarkerwindow import Ui_advancedLineMarkerWindow
from gui_newmarkerwindow import Ui_newMarkerWindow
from gui_systemwindow import Ui_systemWindow
import math
import numpy
import conversions
import pyqtgraph as pg
import ast
import time
from __main__ import *

# Predefining global variables
wavelength_name = "Wave"
amplitude_name = "Amp"
Integration_Limit_1 = ''
Integration_Limit_2 = ''
active_trace_num = ''
trace_a_data = ''
trace_b_data = ''
trace_c_data = ''
trace_d_data = ''
trace_e_data = ''
trace_f_data = ''
frequency_units = 'kHz'


# Main class for the Agilent 86142B OSA
class Agilent86142B(QtWidgets.QWidget, Ui_Agilent86142B):
    def __init__(self, my_instrument, parent=None):
        super(Agilent86142B, self).__init__(parent)
        global instrument1
        instrument1 = my_instrument

        # Calling setup and display functions to set the machine up at the start
        global bootup
        bootup = 1
        instrument1.timeout = 20000 # Sets timeout period for VISA
        self.setupUi(self)
        instrument1.write("INIT:CONT OFF") # Turn continuous sweeps off
        instrument1.write("INIT:IMM;*OPC?") # Take a single sweep
        self.setupInstrument()
        self.setupMarkers()
        self.setupTrace()
        self.infoDisplay()
        instrument1.write("*CLS") # Clear error messages
        self.p1 = pg.PlotWidget() # Add graph widget to GUI to allow plotting
        self.p1.showGrid(x=True, y=True)

        # Pre-allocating empty plots for reference level, line markers and threshold so they can be overwritten later
        global ref_plot
        ref_plot = self.p1.plot(x=[], y=[])
        global line_1_plot
        line_1_plot = self.p1.plot(x=[], y=[])
        global line_2_plot
        line_2_plot = self.p1.plot(x=[], y=[])
        global thresh_plot
        thresh_plot = self.p1.plot(x=[], y=[])
        sweep = 0
        self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
        bootup = 0

        # Pre-allocating empty plots for markers so they can be overwritten later
        global mkr1_plot
        mkr1_plot = self.p1.plot(x=[], y=[])
        global mkr2_plot
        mkr2_plot = self.p1.plot(x=[], y=[])
        global mkr3_plot
        mkr3_plot = self.p1.plot(x=[], y=[])
        global mkr4_plot
        mkr4_plot = self.p1.plot(x=[], y=[])
        global BW_mkr_1_plot_left
        BW_mkr_1_plot_left = self.p1.plot(x=[], y=[])
        global BW_mkr_1_plot_right
        BW_mkr_1_plot_right = self.p1.plot(x=[], y=[])
        global BW_mkr_1_plot_centre
        BW_mkr_1_plot_centre = self.p1.plot(x=[], y=[])
        global noise_mkr_1_plot
        noise_mkr_1_plot = self.p1.plot(x=[], y=[])
        global delta_mkr_1_plot
        delta_mkr_1_plot = self.p1.plot(x=[], y=[])
        global OSNR_mkr_1_plot_left
        OSNR_mkr_1_plot_left = self.p1.plot(x=[], y=[])
        global OSNR_mkr_1_plot_right
        OSNR_mkr_1_plot_right = self.p1.plot(x=[], y=[])
        global OSNR_mkr_1_plot_centre
        OSNR_mkr_1_plot_centre = self.p1.plot(x=[], y=[])

        global BW_mkr_2_plot_left
        BW_mkr_2_plot_left = self.p1.plot(x=[], y=[])
        global BW_mkr_2_plot_right
        BW_mkr_2_plot_right = self.p1.plot(x=[], y=[])
        global BW_mkr_2_plot_centre
        BW_mkr_2_plot_centre = self.p1.plot(x=[], y=[])
        global noise_mkr_2_plot
        noise_mkr_2_plot = self.p1.plot(x=[], y=[])
        global delta_mkr_2_plot
        delta_mkr_2_plot = self.p1.plot(x=[], y=[])
        global OSNR_mkr_2_plot_left
        OSNR_mkr_2_plot_left = self.p1.plot(x=[], y=[])
        global OSNR_mkr_2_plot_right
        OSNR_mkr_2_plot_right = self.p1.plot(x=[], y=[])
        global OSNR_mkr_2_plot_centre
        OSNR_mkr_2_plot_centre = self.p1.plot(x=[], y=[])

        global BW_mkr_3_plot_left
        BW_mkr_3_plot_left = self.p1.plot(x=[], y=[])
        global BW_mkr_3_plot_right
        BW_mkr_3_plot_right = self.p1.plot(x=[], y=[])
        global BW_mkr_3_plot_centre
        BW_mkr_3_plot_centre = self.p1.plot(x=[], y=[])
        global noise_mkr_3_plot
        noise_mkr_3_plot = self.p1.plot(x=[], y=[])
        global delta_mkr_3_plot
        delta_mkr_3_plot = self.p1.plot(x=[], y=[])
        global OSNR_mkr_3_plot_left
        OSNR_mkr_3_plot_left = self.p1.plot(x=[], y=[])
        global OSNR_mkr_3_plot_right
        OSNR_mkr_3_plot_right = self.p1.plot(x=[], y=[])
        global OSNR_mkr_3_plot_centre
        OSNR_mkr_3_plot_centre = self.p1.plot(x=[], y=[])

        global BW_mkr_4_plot_left
        BW_mkr_4_plot_left = self.p1.plot(x=[], y=[])
        global BW_mkr_4_plot_right
        BW_mkr_4_plot_right = self.p1.plot(x=[], y=[])
        global BW_mkr_4_plot_centre
        BW_mkr_4_plot_centre = self.p1.plot(x=[], y=[])
        global noise_mkr_4_plot
        noise_mkr_4_plot = self.p1.plot(x=[], y=[])
        global delta_mkr_4_plot
        delta_mkr_4_plot = self.p1.plot(x=[], y=[])
        global OSNR_mkr_4_plot_left
        OSNR_mkr_4_plot_left = self.p1.plot(x=[], y=[])
        global OSNR_mkr_4_plot_right
        OSNR_mkr_4_plot_right = self.p1.plot(x=[], y=[])
        global OSNR_mkr_4_plot_centre
        OSNR_mkr_4_plot_centre = self.p1.plot(x=[], y=[])

        # Calling OSNRsetup to determine if any markers have the OSNR marker active. Called separately here instead of in the
        # setupInstrument function as it needs to have both trace data and marker data previously defined
        self.OSNRsetup()
        if mkr_1_param[6] == 'ON' and active_marker == '1':
            self.mkr1OSNRDisplay()
        if mkr_2_param[6] == 'ON' and active_marker == '2':
            self.mkr2OSNRDisplay()
        if mkr_3_param[6] == 'ON' and active_marker == '3':
            self.mkr3OSNRDisplay()
        if mkr_4_param[6] == 'ON' and active_marker == '4':
            self.mkr4OSNRDisplay()

        self.markerPlot()
        self.threshPlot()
        self.linemarkerPlot()
        self.threshPlot()
        self.topMenu()
        self.wavelengthMenu()
         
        # Setup mouse events on graph
        mypen = pg.mkPen('y', width=1)
        self.curve = self.p1.plot(x=[], y=[], pen=mypen)
        self.curve.scene().sigMouseMoved.connect(self.onMouseMoved)
        self.p1.scene().sigMouseClicked.connect(self.onMouseClicked)


    def topMenu(self):
        global menuFlag
        menuFlag = 'top'
        # Active buttons for the markers and trace at the top of the interface. Connects to functions further down
        self.buttonActMkrGbl.setText("Mkr %s" %active_marker)
        self.buttonActTrcGbl.setText("Trace %s" %active_trace[2])
        self.buttonDispDisable.setText("%s" %displayDisabled)
        if reset == 0:
            self.menuActMkrGbl = QtWidgets.QMenu()
            self.menuActMkrGbl.addAction("Mkr 1", self.ActMkrGbl1)
            self.menuActMkrGbl.addAction("Mkr 2", self.ActMkrGbl2)
            self.menuActMkrGbl.addAction("Mkr 3", self.ActMkrGbl3)
            self.menuActMkrGbl.addAction("Mkr 4", self.ActMkrGbl4)
            self.buttonActMkrGbl.setMenu(self.menuActMkrGbl)
            self.menuActTrcGbl = QtWidgets.QMenu()
            self.menuActTrcGbl.addAction("Trace A", self.ActTrcGbl1)
            self.menuActTrcGbl.addAction("Trace B", self.ActTrcGbl2)
            self.menuActTrcGbl.addAction("Trace C", self.ActTrcGbl3)
            self.menuActTrcGbl.addAction("Trace D", self.ActTrcGbl4)
            self.menuActTrcGbl.addAction("Trace E", self.ActTrcGbl5)
            self.menuActTrcGbl.addAction("Trace F", self.ActTrcGbl6)
            self.buttonActTrcGbl.setMenu(self.menuActTrcGbl)
            self.menuDispDisable = QtWidgets.QMenu()
            self.menuDispDisable.addAction("OFF", self.DisableDispAction1)
            self.menuDispDisable.addAction("ON", self.DisableDispAction2)
            self.buttonDispDisable.setMenu(self.menuDispDisable)
            self.buttonSystem.clicked.connect(self.systemMenu)
        else:
            self.buttonActMkrGbl.clicked.connect(self.updatingException)
            self.menuActTrcGbl.clicked.connect(self.updatingException)
            self.buttonDispDisable.clicked.connect(self.updatingException)
            self.buttonSystem.clicked.connect(self.updatingException)

        # Top menu buttons clicked
        self.buttonWavelength.clicked.connect(self.wavelengthMenu)
        self.buttonAmplitude.clicked.connect(self.amplitudeMenu)
        self.buttonMarkers.clicked.connect(self.markersMenu)
        self.buttonTraces.clicked.connect(self.tracesMenu)
        self.buttonBW.clicked.connect(self.bwMenu)

        # Bottom menu button clicked
        self.buttonAutoMeasure.clicked.connect(self.autoMeasure)
        self.buttonAutoAlign.clicked.connect(self.autoAlign)
        self.buttonSync.clicked.connect(self.sync)


## ------------------------------------------------------
##          NON-MENU/GLOBAL FUNCTIONS
## ------------------------------------------------------

    # The following functions clear the corresponding marker displays at the top of the display      
    def clearTopText1(self):
        self.topLabel11.setText("")
        self.topLabel12.setText("")
        self.topLabel13.setText("")

    def clearTopText2(self):
        self.topLabel21.setText("")
        self.topLabel22.setText("")
        self.topLabel23.setText("")

    def clearTopText3(self):
        self.topLabel31.setText("")
        self.topLabel32.setText("")
        self.topLabel33.setText("")

    def clearTopText4(self):
        self.topLabel41.setText("")
        self.topLabel42.setText("")
        self.topLabel43.setText("")

    def clearTopText5(self):
        self.topLabel51.setText("")
        self.topLabel52.setText("")
        self.topLabel53.setText("")

    def clearTopText6(self):
        self.topLabel61.setText("")
        self.topLabel62.setText("")
        self.topLabel63.setText("")
    
    # The following functions allow changing of the active markers and active traces. When each function runs it makes it the active marker,
    # turns the marker on and places it on the active trace. It then calls the relevant display function which updates the display and data arrays
    def ActMkrGbl1(self):
        global active_marker
        global mkr_1_param
        global active_mkr_param
        global active_BW_param
        global menuFlag
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        
        self.buttonActMkrGbl.setText("Mkr 1")
        active_marker = '1'
        mkr_1_param[0] = '1'
        trc = mkr_1_param[7]
        instrument1.write("CALCulate:MARKer1:STATe ON")
        instrument1.write("CALCulate:MARKer1:TRACe %s" %trc)
        if mkr_1_param[3] == 'ON':
            self.mkr1BWCalc()
            self.mkr1BWDisplay()
        elif mkr_1_param[4] == 'ON':
            self.mkr1NoiseDisplay()
            self.mkrCompDisplay()
        elif mkr_1_param[5] == 'ON':
            self.mkr1DeltaCalc()
            self.mkr1DeltaDisplay()
        elif mkr_1_param[6] == 'ON':
            self.mkr1OSNRCalc()
            self.mkr1OSNRDisplay()
        else:
            if mkr_2_param[3] == 'ON' or mkr_2_param[4] == 'ON' or mkr_2_param[5] == 'ON' or mkr_2_param[6] == 'ON' or mkr_3_param[3] == 'ON' or mkr_3_param[4] == 'ON' or mkr_3_param[5] == 'ON' or mkr_3_param[6] == 'ON' or mkr_4_param[3] == 'ON' or mkr_4_param[4] == 'ON' or mkr_4_param[5] == 'ON' or mkr_4_param[6] == 'ON':
                self.mkr2NormCalc()
                self.mkr2NormDisplay()
                self.mkr3NormCalc()
                self.mkr3NormDisplay()
                self.mkr4NormCalc()
                self.mkr4NormDisplay()
                self.mkr1NormCalc()
                self.mkr1NormDisplay()
            else:
                self.mkr1NormCalc()
                self.mkr1NormDisplay()
            self.mkrCompDisplay()
        active_mkr_param = mkr_1_param
        active_BW_param = BW_1_param
        self.markerPlot()
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'moreMarkers':
            self.moreMkrFunc()
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ActMkrGbl2(self):
        global active_marker
        global mkr_2_param
        global active_mkr_param
        global active_BW_param
        global menuFlag
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        
        self.buttonActMkrGbl.setText("Mkr 2")
        active_marker = '2'
        mkr_2_param[0] = '1'
        trc = mkr_2_param[7]
        instrument1.write("CALCulate:MARKer2:STATe ON")
        instrument1.write("CALCulate:MARKer2:TRACe %s" %trc)
        if mkr_2_param[3] == 'ON':
            self.mkr2BWCalc()
            self.mkr2BWDisplay()
        elif mkr_2_param[4] == 'ON':
            self.mkr2NoiseDisplay()
            self.mkrCompDisplay()
        elif mkr_2_param[5] == 'ON':
            self.mkr2DeltaCalc()
            self.mkr2DeltaDisplay()
        elif mkr_2_param[6] == 'ON':
            self.mkr2OSNRCalc()
            self.mkr2OSNRDisplay()
        else:
            if mkr_1_param[3] == 'ON' or mkr_1_param[4] == 'ON' or mkr_1_param[5] == 'ON' or mkr_1_param[6] == 'ON' or mkr_3_param[3] == 'ON' or mkr_3_param[4] == 'ON' or mkr_3_param[5] == 'ON' or mkr_3_param[6] == 'ON' or mkr_4_param[3] == 'ON' or mkr_4_param[4] == 'ON' or mkr_4_param[5] == 'ON' or mkr_4_param[6] == 'ON':
                self.mkr1NormCalc()
                self.mkr1NormDisplay()
                self.mkr3NormCalc()
                self.mkr3NormDisplay()
                self.mkr4NormCalc()
                self.mkr4NormDisplay()
                self.mkr2NormCalc()
                self.mkr2NormDisplay()
            else:
                self.mkr2NormCalc()
                self.mkr2NormDisplay()
            self.mkrCompDisplay()
        active_mkr_param = mkr_2_param
        active_BW_param = BW_2_param
        self.markerPlot()
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'moreMarkers':
            self.moreMkrFunc()
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ActMkrGbl3(self):
        global active_marker
        global mkr_3_param
        global active_mkr_param
        global active_BW_param
        global menuFlag
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        
        self.buttonActMkrGbl.setText("Mkr 3")
        active_marker = '3'
        mkr_3_param[0] = '1'
        trc = mkr_3_param[7]
        instrument1.write("CALCulate:MARKer3:STATe ON")
        instrument1.write("CALCulate:MARKer3:TRACe %s" %trc)
        if mkr_3_param[3] == 'ON':
            self.mkr3BWCalc()
            self.mkr3BWDisplay()
        elif mkr_3_param[4] == 'ON':
            self.mkr3NoiseDisplay()
            self.mkrCompDisplay()
        elif mkr_3_param[5] == 'ON':
            self.mkr3DeltaCalc()
            self.mkr3DeltaDisplay()
        elif mkr_3_param[6] == 'ON':
            self.mkr3OSNRCalc()
            self.mkr3OSNRDisplay()
        else:
            if mkr_1_param[3] == 'ON' or mkr_1_param[4] == 'ON' or mkr_1_param[5] == 'ON' or mkr_1_param[6] == 'ON' or mkr_2_param[3] == 'ON' or mkr_2_param[4] == 'ON' or mkr_2_param[5] == 'ON' or mkr_2_param[6] == 'ON' or mkr_4_param[3] == 'ON' or mkr_4_param[4] == 'ON' or mkr_4_param[5] == 'ON' or mkr_4_param[6] == 'ON':
                self.mkr1NormCalc()
                self.mkr1NormDisplay()
                self.mkr2NormCalc()
                self.mkr2NormDisplay()
                self.mkr4NormCalc()
                self.mkr4NormDisplay()
                self.mkr3NormCalc()
                self.mkr3NormDisplay()
            else:
                self.mkr3NormCalc()
                self.mkr3NormDisplay()
            self.mkrCompDisplay()
        active_mkr_param = mkr_3_param
        active_BW_param = BW_3_param
        self.markerPlot()
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'moreMarkers':
            self.moreMkrFunc()
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ActMkrGbl4(self):
        global active_marker
        global mkr_4_param
        global active_mkr_param
        global active_BW_param
        global menuFlag
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            
        self.buttonActMkrGbl.setText("Mkr 4")
        active_marker = '4'
        mkr_4_param[0] = '1'
        trc = mkr_4_param[7]
        instrument1.write("CALCulate:MARKer4:STATe ON")
        instrument1.write("CALCulate:MARKer4:TRACe %s" %trc)
        if mkr_4_param[3] == 'ON':
            self.mkr4BWCalc()
            self.mkr4BWDisplay()
        elif mkr_4_param[4] == 'ON':
            self.mkr4NoiseDisplay()
            self.mkrCompDisplay()
        elif mkr_4_param[5] == 'ON':
            self.mkr4DeltaCalc()
            self.mkr4DeltaDisplay()
        elif mkr_4_param[6] == 'ON':
            self.mkr4OSNRCalc()
            self.mkr4OSNRDisplay()
        else:
            if mkr_1_param[3] == 'ON' or mkr_1_param[4] == 'ON' or mkr_1_param[5] == 'ON' or mkr_1_param[6] == 'ON' or mkr_2_param[3] == 'ON' or mkr_2_param[4] == 'ON' or mkr_2_param[5] == 'ON' or mkr_2_param[6] == 'ON' or mkr_3_param[3] == 'ON' or mkr_3_param[4] == 'ON' or mkr_3_param[5] == 'ON' or mkr_3_param[6] == 'ON':
                self.mkr1NormCalc()
                self.mkr1NormDisplay()
                self.mkr2NormCalc()
                self.mkr2NormDisplay()
                self.mkr3NormCalc()
                self.mkr3NormDisplay()
                self.mkr4NormCalc()
                self.mkr4NormDisplay()
            else:
                self.mkr4NormCalc()
                self.mkr4NormDisplay()
            self.mkrCompDisplay()
        active_mkr_param = mkr_4_param
        active_BW_param = BW_4_param
        self.markerPlot()
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'moreMarkers':
            self.moreMkrFunc()
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ActTrcGbl1(self):
        global active_trace
        global active_trace_num
        global trace_a_param
        global active_trace_param
        global menuFlag
        global inUse
        global plotDone
        global reset
          
        self.buttonActTrcGbl.setText("Trace A")
        active_trace = "TRA"
        active_trace_num = '1'
        active_trace_param = trace_a_param
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'traces':
            self.tracesMenu()

    def ActTrcGbl2(self):
        global active_trace
        global active_trace_num
        global trace_b_param
        global active_trace_param
        global menuFlag
        
        self.buttonActTrcGbl.setText("Trace B")
        active_trace = "TRB"
        active_trace_num = '2'
        active_trace_param = trace_b_param
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'traces':
            self.tracesMenu()

    def ActTrcGbl3(self):
        global active_trace
        global active_trace_num
        global trace_c_param
        global active_trace_param
        global menuFlag
        
        self.buttonActTrcGbl.setText("Trace C")
        active_trace = "TRC"
        active_trace_num = '3'
        active_trace_param = trace_c_param
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'traces':
            self.tracesMenu()

    def ActTrcGbl4(self):
        global active_trace
        global active_trace_num
        global trace_d_param
        global active_trace_param
        global menuFlag
        
        self.buttonActTrcGbl.setText("Trace D")
        active_trace = "TRD"
        active_trace_num = '4'
        active_trace_param = trace_d_param
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'traces':
            self.tracesMenu()

    def ActTrcGbl5(self):
        global active_trace
        global active_trace_num
        global trace_e_param
        global active_trace_param
        global menuFlag
        
        self.buttonActTrcGbl.setText("Trace E")
        active_trace = "TRE"
        active_trace_num = '5'
        active_trace_param = trace_e_param
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'traces':
            self.tracesMenu()
            
    def ActTrcGbl6(self):
        global active_trace
        global active_trace_num
        global trace_f_param
        global active_trace_param
        global menuFlag
        
        self.buttonActTrcGbl.setText("Trace F")
        active_trace = "TRF"
        active_trace_num = '6'
        active_trace_param = trace_f_param
        if menuFlag == 'markers':
            self.markersMenu()
        if menuFlag == 'traces':
            self.tracesMenu()

    # Function to transfer active marker parameters back into corresponding marker parameters array
    def updateMkrParam(self):
        global active_marker
        global active_mkr_param
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param

        if active_marker == '1':
            mkr_1_param = active_mkr_param
            BW_1_param = active_BW_param
        if active_marker == '2':
            mkr_2_param = active_mkr_param
            BW_2_param = active_BW_param
        if active_marker == '3':
            mkr_3_param = active_mkr_param
            BW_3_param = active_BW_param
        if active_marker == '4':
            mkr_4_param = active_mkr_param
            BW_4_param = active_BW_param

    # Function to transfer active trace parameters back into corresponding trace parameters array
    def updateTrcParam(self):
        global active_trace_num
        global trace_a_param
        global trace_b_param
        global trace_c_param
        global trace_d_param
        global trace_e_param
        global trace_f_param

        if active_trace_num == '1':
            trace_a_param = active_trace_param
        if active_trace_num == '2':
            trace_b_param = active_trace_param
        if active_trace_num == '3':
            trace_c_param = active_trace_param
        if active_trace_num == '4':
            trace_d_param = active_trace_param
        if active_trace_num == '5':
            trace_e_param = active_trace_param
        if active_trace_num == '6':
            trace_f_param = active_trace_param

    # Automeasure function. Contains a check to ensure that the button was pressed correctly        
    def autoMeasure(self):
        if repeatSweepOnOff == 'ON':
            self.sweepException()
        else:
            widget = ConfirmDialog("Auto Measure")
            widget.exec_()
            if widget.userInput == 1:
                instrument1.write("DISPlay:WINDow:TRACe:ALL:SCALe:AUTO")

    # Automeasure function. Contains a check to ensure that the button was pressed correctly   
    def autoAlign(self):
        if repeatSweepOnOff == 'ON':
            self.sweepException()
        else:
            widget = ConfirmDialog("Auto Align")
            widget.exec_()
            if widget.userInput == 1:
                instrument1.write("CALibration:ALIGn")

    # Turning machine display off will speed up marker and trace calls
    def DisableDispAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonDispDisable.setText("OFF")
        instrument1.write("DISPlay:WINDow OFF")
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    # Turn actual machine display back on
    def DisableDispAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonDispDisable.setText("ON")
        instrument1.write("DISPlay:WINDow ON")
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Function to synchronise machine and software if the user changes paramters on the actual machine while software is still running
    def sync(self):
        if repeatSweepOnOff == 'ON':
            self.sweepException()
        else:
            widget = ConfirmDialog("Device Sync")
            widget.exec_()
            if widget.userInput == 1:
                self.setupInstrument()
                self.setupMarkers()
                self.setupTrace()
                self.OSNRsetup()
                sweep = 1
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                                 trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                                 trace_d_param, trace_e_param, trace_f_param, sweep)
                self.markerPlot()
                self.infoDisplay()

    # Pulls up the system configuration window
    def systemMenu(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        widget = SystemWindow()
        widget.exec_()
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0

        
## ------------------------------------------------------
##      GRAPH INTERACTION FUNCTIONS
## ------------------------------------------------------

    # Function to use the left and right arrow keys to move the active marker left or right along the trace.
    # Indent_margin variable defines how far the marker moves on each key press and can be changed in the system menu

    def keyPressEvent(self, event):
        global indent_margin
        global inUse
        global plotDone
        global reset
        global mkr_1_index
        global mkr_2_index
        global mkr_3_index
        global mkr_4_index
        global repeatSweepOnOff

        if active_trace == "TRA":
            traceX = traceA[:,0]
            traceY = traceA[:,1]
        elif active_trace == "TRB":
            traceX = traceB[:,0]
            traceY = traceB[:,1]
        elif active_trace == "TRC":
            traceX = traceC[:,0]
            traceY = traceC[:,1]
        elif active_trace == "TRD":
            traceX = traceD[:,0]
            traceY = traceD[:,1]
        elif active_trace == "TRE":
            traceX = traceE[:,0]
            traceY = traceE[:,1]
        elif active_trace == "TRF":
            traceX = traceF[:,0]
            traceY = traceF[:,1]
        key = event.key()

        if repeatSweepOnOff == 'ON':
            if active_mkr_param[3] == 'OFF' and active_mkr_param[4] == 'OFF' and active_mkr_param[5] == 'OFF' and active_mkr_param[6] == 'OFF':
                if key == QtCore.Qt.Key_Left:
                    if active_marker == '1':
                        mkr_1_index = mkr_1_index - indent_margin
                        index = mkr_1_index
                    elif active_marker == '2':
                        mkr_2_index = mkr_2_index - indent_margin
                        index = mkr_2_index
                    elif active_marker == '3':
                        mkr_3_index = mkr_3_index - indent_margin
                        index = mkr_3_index
                    elif active_marker == '4':
                        mkr_4_index = mkr_4_index - indent_margin
                        index = mkr_4_index
                    else:
                        index = 500
                elif key == QtCore.Qt.Key_Right:
                    if active_marker == '1':
                        mkr_1_index = mkr_1_index + indent_margin
                        index = mkr_1_index
                    elif active_marker == '2':
                        mkr_2_index = mkr_2_index + indent_margin
                        index = mkr_2_index
                    elif active_marker == '3':
                        mkr_3_index = mkr_3_index + indent_margin
                        index = mkr_3_index
                    elif active_marker == '4':
                        mkr_4_index = mkr_4_index + indent_margin
                        index = mkr_4_index
                    else:
                        index = 500
                    
                markerX = conversions.str2float(traceX[index],wavelength_units)
                markerY = float(traceY[index])
                if active_marker == '1':
                    mkr_1_param[1] = markerX
                    mkr_1_param[2] = markerY
                    self.mkr1NormDisplay()
                    self.mkrCompDisplay()
                elif active_marker == '2':
                    mkr_2_param[1] = markerX
                    mkr_2_param[2] = markerY
                    self.mkr2NormDisplay()
                    self.mkrCompDisplay()
                elif active_marker == '3':
                    mkr_3_param[1] = markerX
                    mkr_3_param[2] = markerY
                    self.mkr3NormDisplay()
                    self.mkrCompDisplay()
                elif active_marker == '4':
                    mkr_4_param[1] = markerX
                    mkr_4_param[2] = markerY
                    self.mkr4NormDisplay()
                    self.mkrCompDisplay()
                self.markerPlot()

        else:
            markerX = float(instrument1.query("CALCulate:MARKer%s:X?" %active_marker))

            # Find the marker position in the trace data to obtain and index value
            i = 0
            error_thresh = 0.01
            for i in range(len(traceX)):
                distance_x = abs(traceX[i]-markerX)
                if distance_x < error_thresh:
                    index = i
                    error_thresh = distance_x
    
            # Left key press      
            if key == QtCore.Qt.Key_Left:
                index = index - indent_margin
                trace_x_val = str(conversions.str2float(traceX[index],wavelength_units))
                trace_y_val = str(conversions.str2float(traceY[index],amplitude_units))
                instrument1.write("CALCulate:MARKer%s:X %s%s" %(active_marker,trace_x_val,wavelength_units))
                instrument1.write("CALCulate:MARKer%s:TRACe %s" %(active_marker,active_trace))
                if active_marker == "1":
                    if mkr_1_param[3] == 'ON':
                        self.mkr1NormCalc()
                        self.mkr1BWCalc()
                        self.mkr1BWDisplay()
                    elif mkr_1_param[5] == 'ON':
                        self.mkr1DeltaCalc()
                        self.mkr1DeltaDisplay()
                    elif mkr_1_param[6] == 'ON':
                        self.mkr1NormCalc()
                        self.mkr1OSNRCalc()
                        self.mkr1OSNRDisplay()
                    else:
                        self.mkr1NormCalc()
                        self.mkr1NormDisplay()
                        self.mkrCompDisplay()
                elif active_marker == "2":
                    if mkr_2_param[3] == 'ON':
                        self.mkr2NormCalc()
                        self.mkr2BWCalc()
                        self.mkr2BWDisplay()
                    elif mkr_2_param[5] == 'ON':
                        self.mkr2DeltaCalc()
                        self.mkr2DeltaDisplay()
                    elif mkr_2_param[6] == 'ON':
                        self.mkr2NormCalc()
                        self.mkr2OSNRCalc()
                        self.mkr2OSNRDisplay()
                    else:
                        self.mkr2NormCalc()
                        self.mkr2NormDisplay()
                        self.mkrCompDisplay()
                elif active_marker == "3":
                    if mkr_3_param[3] == 'ON':
                        self.mkr3NormCalc()
                        self.mkr3BWCalc()
                        self.mkr3BWDisplay()
                    elif mkr_3_param[5] == 'ON':
                        self.mkr3DeltaCalc()
                        self.mkr3DeltaDisplay()
                    elif mkr_3_param[6] == 'ON':
                        self.mkr3NormCalc()
                        self.mkr3OSNRCalc()
                        self.mkr3OSNRDisplay()
                    else:
                        self.mkr3NormCalc()
                        self.mkr3NormDisplay()
                        self.mkrCompDisplay()
                elif active_marker == "4":
                    if mkr_4_param[3] == 'ON':
                        self.mkr4NormCalc()
                        self.mkr4BWCalc()
                        self.mkr4BWDisplay()
                    elif mkr_4_param[5] == 'ON':
                        self.mkr4DeltaCalc()
                        self.mkr4DeltaDisplay()
                    elif mkr_4_param[6] == 'ON':
                        self.mkr4NormCalc()
                        self.mkr4OSNRCalc()
                        self.mkr4OSNRDisplay()
                    else:
                        self.mkr4NormCalc()
                        self.mkr4NormDisplay()
                        self.mkrCompDisplay()
                self.markerPlot()

            # Right key press
            if key == QtCore.Qt.Key_Right:
                index = index + indent_margin
                trace_x_val = str(conversions.str2float(traceX[index],wavelength_units))
                trace_y_val = str(conversions.str2float(traceY[index],amplitude_units))
                instrument1.write("CALCulate:MARKer%s:X %s%s" %(active_marker,trace_x_val,wavelength_units))
                instrument1.write("CALCulate:MARKer%s:TRACe %s" %(active_marker,active_trace))
                if active_marker == "1":
                    if mkr_1_param[3] == 'ON':
                        self.mkr1NormCalc()
                        self.mkr1BWCalc()
                        self.mkr1BWDisplay()
                    elif mkr_1_param[5] == 'ON':
                        self.mkr1DeltaCalc()
                        self.mkr1DeltaDisplay()
                    elif mkr_1_param[6] == 'ON':
                        self.mkr1NormCalc()
                        self.mkr1OSNRCalc()
                        self.mkr1OSNRDisplay()
                    else:
                        self.mkr1NormCalc()
                        self.mkr1NormDisplay()
                        self.mkrCompDisplay()
                elif active_marker == "2":
                    if mkr_2_param[3] == 'ON':
                        self.mkr2NormCalc()
                        self.mkr2BWCalc()
                        self.mkr2BWDisplay()
                    elif mkr_2_param[5] == 'ON':
                        self.mkr2DeltaCalc()
                        self.mkr2DeltaDisplay()
                    elif mkr_2_param[6] == 'ON':
                        self.mkr2NormCalc()
                        self.mkr2OSNRCalc()
                        self.mkr2OSNRDisplay()
                    else:
                        self.mkr2NormCalc()
                        self.mkr2NormDisplay()
                        self.mkrCompDisplay()
                elif active_marker == "3":
                    if mkr_3_param[3] == 'ON':
                        self.mkr3NormCalc()
                        self.mkr3BWCalc()
                        self.mkr3BWDisplay()
                    elif mkr_3_param[5] == 'ON':
                        self.mkr3DeltaCalc()
                        self.mkr3DeltaDisplay()
                    elif mkr_3_param[6] == 'ON':
                        self.mkr3NormCalc()
                        self.mkr3OSNRCalc()
                        self.mkr3OSNRDisplay()
                    else:
                        self.mkr3NormCalc()
                        self.mkr3NormDisplay()
                        self.mkrCompDisplay()
                elif active_marker == "4":
                    if mkr_4_param[3] == 'ON':
                        self.mkr4NormCalc()
                        self.mkr4BWCalc()
                        self.mkr4BWDisplay()
                    elif mkr_4_param[5] == 'ON':
                        self.mkr4DeltaCalc()
                        self.mkr4DeltaDisplay()
                    elif mkr_4_param[6] == 'ON':
                        self.mkr4NormCalc()
                        self.mkr4OSNRCalc()
                        self.mkr4OSNRDisplay()
                    else:
                        self.mkr4NormCalc()
                        self.mkr4NormDisplay()
                        self.mkrCompDisplay()
                self.markerPlot()

    # OnMouseMoved follows the movement of the mouse and maps the scene coordinates to viewBox coordinates
    def onMouseMoved(self, point):
        global p
        p = self.p1.plotItem.vb.mapSceneToView(point)

    # onMouseClicked allows the user to place a marker on a trace with a mouse click.
    def onMouseClicked(self, event):
        global active_marker
        global active_trace
        global traceA
        global traceB
        global traceC
        global traceD
        global traceE
        global traceF
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param
        global inUse
        global plotDone
        global reset
        global contOnOff
        
        buttons = event.button()
        if buttons == 1:
            inUse = 1
            if repeatSweepOnOff == "ON":
                while plotDone == 0:
                    pass
                instrument1.write("INITiate:CONTinuous 0")
                contOnOff = 0
            widget = NewMarkerWindow(active_marker, active_trace, trace_a_param, trace_b_param, trace_c_param, trace_d_param, trace_e_param, trace_f_param)
            widget.exec_()
            if widget.selection != 0:
                if widget.trace == 'Trace A':
                    self.ActTrcGbl1()
                if widget.trace == 'Trace B':
                    self.ActTrcGbl2()
                if widget.trace == 'Trace C':
                    self.ActTrcGbl3()
                if widget.trace == 'Trace D':
                    self.ActTrcGbl4()
                if widget.trace == 'Trace E':
                    self.ActTrcGbl5()
                if widget.trace == 'Trace F':
                    self.ActTrcGbl6()

                if widget.marker == 'Mkr 1':
                    active_marker = '1'
                    active_mkr_param = mkr_1_param
                    mkr_1_param[0] = '1'
                if widget.marker == 'Mkr 2':
                    active_marker = '2'
                    active_mkr_param = mkr_2_param
                    mkr_2_param[0] = '1'
                if widget.marker == 'Mkr 3':
                    active_marker = '3'
                    active_mkr_param = mkr_3_param
                    mkr_3_param[0] = '1'
                if widget.marker == 'Mkr 4':
                    active_marker = '4'
                    active_mkr_param = mkr_4_param
                    mkr_4_param[0] = '1'

                # Obtaining data for the active trace
                if active_trace == 'TRA':
                    trace_data = traceA
                    self.ActTrcGbl1()
                if active_trace == 'TRB':
                    trace_data = traceB
                    self.ActTrcGbl2()
                if active_trace == 'TRC':
                    trace_data = traceC
                    self.ActTrcGbl3()
                if active_trace == 'TRD':
                    trace_data = traceD
                    self.ActTrcGbl4()
                if active_trace == 'TRE':
                    trace_data = traceE
                    self.ActTrcGbl5()
                if active_trace == 'TRF':
                    trace_data = traceF
                    self.ActTrcGbl6()

                trace_x = trace_data[:,0]
                trace_y = trace_data[:,1]
               
                # To determine where the marker needs to be plotted, we find the place in the active trace data
                # which is closest to the chosen marker position on graph
                error_thresh = 0.01 
                for i in range(len(trace_x)):
                    distance_x = abs(trace_x[i]-p.x())
                    if distance_x < error_thresh:
                        mkr_index = i
                        error_thresh = distance_x

                marker_x_write = "CALCulate:MARKer%s:X %sm" %(active_marker,trace_x[mkr_index])
                instrument1.write(marker_x_write)
                instrument1.write("CALCulate:MARKer%s:TRACe %s" %(active_marker,active_trace))

                if active_marker == '1':
                    self.buttonActMkrGbl.setText("Mkr 1")
                    mkr_1_param[7] = active_trace
                    if mkr_1_param[3] == 'ON':
                        self.mkr1NormCalc()
                        #self.mkr1NormDisplay()
                        self.mkr1BWCalc()
                        self.mkr1BWDisplay()
                    elif mkr_1_param[4] == 'ON':
                        self.mkr1NormCalc()
                        self.mkr1NoiseDisplay()
                    elif mkr_1_param[5] == 'ON':
                        self.mkr1DeltaCalc()
                        self.mkr1DeltaDisplay()
                    elif mkr_1_param[6] == 'ON':
                        self.mkr1NormCalc()
                        #self.mkr1NormDisplay()
                        self.mkr1OSNRCalc()
                        self.mkr1OSNRDisplay()
                    else:
                        self.mkr1NormCalc()
                        self.mkr1NormDisplay()
                        self.mkr2NormDisplay()
                        self.mkr3NormDisplay()
                        self.mkr4NormDisplay()
                        self.mkrCompDisplay()
                if active_marker == '2':
                    self.buttonActMkrGbl.setText("Mkr 2")
                    mkr_2_param[7] = active_trace
                    if mkr_2_param[3] == 'ON':
                        self.mkr2NormCalc()
                        #self.mkr2NormDisplay()
                        self.mkr2BWCalc()
                        self.mkr2BWDisplay()
                    elif mkr_2_param[4] == 'ON':
                        self.mkr2NormCalc()
                        self.mkr2NoiseDisplay()
                    elif mkr_2_param[5] == 'ON':
                        self.mkr2DeltaCalc()
                        self.mkr2DeltaDisplay()
                    elif mkr_2_param[6] == 'ON':
                        self.mkr2NormCalc()
                        #self.mkr2NormDisplay()
                        self.mkr2OSNRCalc()
                        self.mkr2OSNRDisplay()
                    else:
                        self.mkr2NormCalc()
                        self.mkr1NormDisplay()
                        self.mkr2NormDisplay()
                        self.mkr3NormDisplay()
                        self.mkr4NormDisplay()
                        self.mkrCompDisplay()
                if active_marker == '3':
                    self.buttonActMkrGbl.setText("Mkr 3")
                    mkr_3_param[7] = active_trace
                    if mkr_3_param[3] == 'ON':
                        self.mkr3NormCalc()
                        #self.mkr3NormDisplay()
                        self.mkr3BWCalc()
                        self.mkr3BWDisplay()
                    elif mkr_3_param[4] == 'ON':
                        self.mkr3NormCalc()
                        self.mkr3NoiseDisplay()
                    elif mkr_3_param[5] == 'ON':
                        self.mkr3DeltaCalc()
                        self.mkr3DeltaDisplay()
                    elif mkr_3_param[6] == 'ON':
                        self.mkr3NormCalc()
                        #self.mkr3NormDisplay()
                        self.mkr3OSNRCalc()
                        self.mkr3OSNRDisplay()
                    else:
                        self.mkr3NormCalc()
                        self.mkr1NormDisplay()
                        self.mkr2NormDisplay()
                        self.mkr3NormDisplay()
                        self.mkr4NormDisplay()
                        self.mkrCompDisplay()
                if active_marker == '4':
                    self.buttonActMkrGbl.setText("Mkr 4")
                    mkr_4_param[7] = active_trace
                    if mkr_4_param[3] == 'ON':
                        self.mkr4NormCalc()
                        #self.mkr4NormDisplay()
                        self.mkr4BWCalc()
                        self.mkr4BWDisplay()
                    elif mkr_4_param[4] == 'ON':
                        self.mkr4NormCalc()
                        self.mkr4NoiseDisplay()
                    elif mkr_4_param[5] == 'ON':
                        self.mkr4DeltaCalc()
                        self.mkr4DeltaDisplay()
                    elif mkr_4_param[6] == 'ON':
                        self.mkr4NormCalc()
                        #self.mkr4NormDisplay()
                        self.mkr4OSNRCalc()
                        self.mkr4OSNRDisplay()
                    else:
                        self.mkr4NormCalc()
                        self.mkr1NormDisplay()
                        self.mkr2NormDisplay()
                        self.mkr3NormDisplay()
                        self.mkr4NormDisplay()
                        self.mkrCompDisplay()
            
                self.markerPlot()
                if active_mkr_param[3] == 'OFF' and active_mkr_param[4] == 'OFF' and active_mkr_param[5] == 'OFF' and active_mkr_param[6] == 'OFF':
                    self.mkrCompDisplay()
                if repeatSweepOnOff == "ON":
                    reset = 1
            if repeatSweepOnOff == "ON":
                self.goToMenu()
                contOnOff = 1
                instrument1.write("INITiate:CONTinuous 1")
                self.sweepThreadOn()
            inUse = 0
        
    def convertUnits(self, x_value, mkr_type, mkr_unit):
        if mkr_type == 'mkr':
            if mkr_unit == 'nm':
                conversion = x_value * 0.000000001
            elif mkr_unit == 'um':
                conversion = x_value * 0.000001
            elif mkr_unit == 'GHz':
                conversion = (299,792,458/x_value)/1000000000
            elif mkr_unit == 'THz':
                conversion = (299,792,458/x_value)/1000000000000
            elif mkr_unit == 'Ang':
                conversions = x_value * 0.0000000001
        if mkr_type == 'BW':
            if mkr_unit == 'nm':
                conversion = x_value * 0.000000001
            elif mkr_unit == 'um':
                conversion = x_value * 0.000001
            elif mkr_unit == 'GHz':
                conversion = (299,792,458/x_value)/1000000000
            elif mkr_unit == 'THz':
                conversion = (299,792,458/x_value)/1000000000000
            elif mkr_unit == 'Ang':
                conversions = x_value * 0.0000000001
        if mkr_type == 'delta':
            if mkr_unit == 'nm':
                conversion = x_value * 0.000000001
            elif mkr_unit == 'um':
                conversion = x_value * 0.000001
            elif mkr_unit == 'GHz':
                conversion = (299,792,458/x_value)/1000000000
            elif mkr_unit == 'THz':
                conversion = (299,792,458/x_value)/1000000000000
            elif mkr_unit == 'Ang':
                conversions = x_value * 0.0000000001
        if mkr_type == 'OSNR':
            if mkr_unit == 'nm':
                conversion = x_value * 0.000000001
            elif mkr_unit == 'um':
                conversion = x_value * 0.000001
            elif mkr_unit == 'GHz':
                conversion = (299,792,458/x_value)/1000000000
            elif mkr_unit == 'THz':
                conversion = (299,792,458/x_value)/1000000000000
            elif mkr_unit == 'Ang':
                conversions = x_value * 0.0000000001
        return conversion


## ------------------------------------------------------
##      MARKER/TRACE GRAPH DISPLAY FUNCTIONS
## ------------------------------------------------------

    # Marker plot is the main function to draw the markers on the display. The active marker will be shown in white
    # and the rest of the markers will be shown in green
    def markerPlot(self):
        global mkr_units
        global BW_units
        global delta_units
        global active_marker
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param
        global mkr1Colour
        global mkr2Colour
        global mkr3Colour
        global mkr4Colour
        global mkr1_plot
        global mkr2_plot
        global mkr3_plot
        global mkr4_plot
        global BW_1_param
        global BW_2_param
        global BW_3_param
        global BW_4_param
        global BW_mkr_1_plot_left
        global BW_mkr_1_plot_right
        global BW_mkr_1_plot_centre
        global BW_mkr_2_plot_left
        global BW_mkr_2_plot_right
        global BW_mkr_2_plot_centre
        global BW_mkr_3_plot_left
        global BW_mkr_3_plot_right
        global BW_mkr_3_plot_centre
        global BW_mkr_4_plot_left
        global BW_mkr_4_plot_right
        global BW_mkr_4_plot_centre
        global noise_mkr_1_plot
        global noise_mkr_2_plot
        global noise_mkr_3_plot
        global noise_mkr_4_plot
        global delta_1_param
        global delta_2_param
        global delta_3_param
        global delta_4_param
        global delta_mkr_1_plot
        global delta_mkr_2_plot
        global delta_mkr_3_plot
        global delta_mkr_4_plot
        global OSNR_1_param
        global OSNR_2_param
        global OSNR_3_param
        global OSNR_4_param
        global OSNR_mkr_1_plot_left
        global OSNR_mkr_1_plot_right
        global OSNR_mkr_1_plot_centre
        global OSNR_mkr_2_plot_left
        global OSNR_mkr_2_plot_right
        global OSNR_mkr_2_plot_centre
        global OSNR_mkr_3_plot_left
        global OSNR_mkr_3_plot_right
        global OSNR_mkr_3_plot_centre
        global OSNR_mkr_4_plot_left
        global OSNR_mkr_4_plot_right
        global OSNR_mkr_4_plot_centre
        viewMkr1 = 0
        viewMkr2 = 0
        viewMkr3 = 0
        viewMkr4 = 0

        if active_marker == '1':
            mkr1Colour = 'w'
            mkr2Colour = 'g'
            mkr3Colour = 'g'
            mkr4Colour = 'g'
        if active_marker == '2':
            mkr1Colour = 'g'
            mkr2Colour = 'w'
            mkr3Colour = 'g'
            mkr4Colour = 'g'
        if active_marker == '3':
            mkr1Colour = 'g'
            mkr2Colour = 'g'
            mkr3Colour = 'w'
            mkr4Colour = 'g'
        if active_marker == '4':
            mkr1Colour = 'g'
            mkr2Colour = 'g'
            mkr3Colour = 'g'
            mkr4Colour = 'w'

        if mkr_1_param[2] > -250:
            if mkr_1_param[7] == 'TRA':
                if trace_a_param[1] == 'ON':
                    viewMkr1 = 1
            elif mkr_1_param[7] == 'TRB':
                if trace_b_param[1] == 'ON':
                    viewMkr1 = 1
            elif mkr_1_param[7] == 'TRC':
                if trace_c_param[1] == 'ON':
                    viewMkr1 = 1
            elif mkr_1_param[7] == 'TRD':
                if trace_d_param[1] == 'ON':
                    viewMkr1 = 1
            elif mkr_1_param[7] == 'TRE':
                if trace_e_param[1] == 'ON':
                    viewMkr1 = 1
            elif mkr_1_param[7] == 'TRF':
                if trace_f_param[1] == 'ON':
                    viewMkr1 = 1

        if mkr_2_param[2] > -250:
            if mkr_2_param[7] == 'TRA':
                if trace_a_param[1] == 'ON':
                    viewMkr2 = 1
            elif mkr_2_param[7] == 'TRB':
                if trace_b_param[1] == 'ON':
                    viewMkr2 = 1
            elif mkr_2_param[7] == 'TRC':
                if trace_c_param[1] == 'ON':
                    viewMkr2 = 1
            elif mkr_2_param[7] == 'TRD':
                if trace_d_param[1] == 'ON':
                    viewMkr2 = 1
            elif mkr_2_param[7] == 'TRE':
                if trace_e_param[1] == 'ON':
                    viewMkr2 = 1
            elif mkr_2_param[7] == 'TRF':
                if trace_f_param[1] == 'ON':
                    viewMkr2 = 1

        if mkr_3_param[2] > -250:
            if mkr_3_param[7] == 'TRA':
                if trace_a_param[1] == 'ON':
                    viewMkr3 = 1
            elif mkr_3_param[7] == 'TRB':
                if trace_b_param[1] == 'ON':
                    viewMkr3 = 1
            elif mkr_3_param[7] == 'TRC':
                if trace_c_param[1] == 'ON':
                    viewMkr3 = 1
            elif mkr_3_param[7] == 'TRD':
                if trace_d_param[1] == 'ON':
                    viewMkr3 = 1
            elif mkr_3_param[7] == 'TRE':
                if trace_e_param[1] == 'ON':
                    viewMkr3 = 1
            elif mkr_3_param[7] == 'TRF':
                if trace_f_param[1] == 'ON':
                    viewMkr3 = 1

        if mkr_4_param[2] > -250:
            if mkr_4_param[7] == 'TRA':
                if trace_a_param[1] == 'ON':
                    viewMkr4 = 1
            elif mkr_4_param[7] == 'TRB':
                if trace_b_param[1] == 'ON':
                    viewMkr4 = 1
            elif mkr_4_param[7] == 'TRC':
                if trace_c_param[1] == 'ON':
                    viewMkr4 = 1
            elif mkr_4_param[7] == 'TRD':
                if trace_d_param[1] == 'ON':
                    viewMkr4 = 1
            elif mkr_4_param[7] == 'TRE':
                if trace_e_param[1] == 'ON':
                    viewMkr4 = 1
            elif mkr_4_param[7] == 'TRF':
                if trace_f_param[1] == 'ON':
                    viewMkr4 = 1

        if mkr_1_param[0] == '1' and viewMkr1 == 1:
            if mkr_1_param[3] == 'ON':
                self.p1.removeItem(mkr1_plot)
                self.p1.removeItem(BW_mkr_1_plot_left)
                self.p1.removeItem(BW_mkr_1_plot_right)
                self.p1.removeItem(BW_mkr_1_plot_centre)
                BW_mkr_1_plot_left = self.p1.plot([self.convertUnits(BW_1_param[0], 'BW', BW_units)], [BW_1_param[3]], symbol='o', symbolPen=mkr1Colour, symbolBrush=None, name='BW Mkr 1 Left')
                BW_mkr_1_plot_right = self.p1.plot([self.convertUnits(BW_1_param[1], 'BW', BW_units)], [BW_1_param[4]], symbol='o', symbolPen=mkr1Colour, symbolBrush=None, name='BW Mkr 1 Right')
                BW_mkr_1_plot_centre = self.p1.plot([self.convertUnits(mkr_1_param[1], 'BW', BW_units)], [mkr_1_param[2]], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='BW Mkr 1 Centre')
            elif mkr_1_param[3] == 'OFF':
                self.p1.removeItem(mkr1_plot)
                self.p1.removeItem(BW_mkr_1_plot_left)
                self.p1.removeItem(BW_mkr_1_plot_right)
                self.p1.removeItem(BW_mkr_1_plot_centre)
                x_data = self.convertUnits(mkr_1_param[1], 'mkr', mkr_units)
                y_data = mkr_1_param[2]
                mkr1_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='Mkr 1')
                BW_mkr_1_plot_left = self.p1.plot(x=[], y=[])
                BW_mkr_1_plot_right = self.p1.plot(x=[], y=[])
                BW_mkr_1_plot_centre = self.p1.plot(x=[], y=[])
            if mkr_1_param[4] == 'ON':
                self.p1.removeItem(mkr1_plot)
                self.p1.removeItem(noise_mkr_1_plot)
                x_data = self.convertUnits(mkr_1_param[1], 'mkr', mkr_units)
                y_data = mkr_1_param[2]
                noise_mkr_1_plot = self.p1.plot([x_data], [y_data], symbol='s', symbolPen=mkr1Colour, symbolBrush=None, name='Noise Mkr 1')
            elif mkr_1_param[4] == 'OFF':
                if mkr_1_param[3] == 'ON':
                    self.p1.removeItem(noise_mkr_1_plot)
                    noise_mkr_1_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr1_plot)
                    self.p1.removeItem(noise_mkr_1_plot)
                    x_data = self.convertUnits(mkr_1_param[1], 'mkr', mkr_units)
                    y_data = mkr_1_param[2]
                    mkr1_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='Mkr 1')
                    noise_mkr_1_plot = self.p1.plot(x=[], y=[])
            if mkr_1_param[5] == 'ON':
                self.p1.removeItem(mkr1_plot)
                self.p1.removeItem(delta_mkr_1_plot)
                mkr1_plot = self.p1.plot([self.convertUnits(delta_1_param[2], 'delta', delta_units)], [delta_1_param[3]], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='Mkr 1')
                delta_mkr_1_plot = self.p1.plot([self.convertUnits(delta_1_param[0], 'delta', delta_units)], [delta_1_param[1]], symbol='o', symbolPen=mkr1Colour, symbolBrush=None, name='Delta Mkr 1')
            elif mkr_1_param[5] == 'OFF':
                if mkr_1_param[4] == 'ON' or mkr_1_param[3] == 'ON':
                    self.p1.removeItem(delta_mkr_1_plot)
                    delta_mkr_1_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr1_plot)
                    self.p1.removeItem(delta_mkr_1_plot)
                    x_data = self.convertUnits(mkr_1_param[1], 'mkr', mkr_units)
                    y_data = mkr_1_param[2]
                    mkr1_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='Mkr 1')
                    delta_mkr_1_plot = self.p1.plot(x=[], y=[])
            if mkr_1_param[6] == 'ON':
                self.p1.removeItem(mkr1_plot)
                self.p1.removeItem(OSNR_mkr_1_plot_left)
                self.p1.removeItem(OSNR_mkr_1_plot_right)
                self.p1.removeItem(OSNR_mkr_1_plot_centre)
                mkr1_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='Mkr 1')
                OSNR_mkr_1_plot_left = self.p1.plot([self.convertUnits(OSNR_1_param[0], 'mkr', mkr_units)], [OSNR_1_param[1]], symbol='s', symbolPen=mkr1Colour, symbolBrush=None, name='OSNR Mkr 1 Left')
                OSNR_mkr_1_plot_right = self.p1.plot([self.convertUnits(OSNR_1_param[2], 'mkr', mkr_units)], [OSNR_1_param[3]], symbol='s', symbolPen=mkr1Colour, symbolBrush=None, name='OSNR Mkr 1 Right')
                OSNR_mkr_1_plot_centre = self.p1.plot([self.convertUnits(OSNR_1_param[4], 'mkr', mkr_units)],[OSNR_1_param[5]], symbol='o', symbolPen=mkr1Colour, symbolBrush=None, name='OSNR Mkr 1 Centre')
            elif mkr_1_param[6] == 'OFF':
                if mkr_1_param[5] == 'ON' or mkr_1_param[4] == 'ON' or mkr_1_param[3] == 'ON':
                    self.p1.removeItem(OSNR_mkr_1_plot_left)
                    self.p1.removeItem(OSNR_mkr_1_plot_right)
                    self.p1.removeItem(OSNR_mkr_1_plot_centre)
                    OSNR_mkr_1_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_1_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_1_plot_centre = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr1_plot)
                    self.p1.removeItem(OSNR_mkr_1_plot_left)
                    self.p1.removeItem(OSNR_mkr_1_plot_right)
                    self.p1.removeItem(OSNR_mkr_1_plot_centre)
                    x_data = self.convertUnits(mkr_1_param[1], 'mkr', mkr_units)
                    y_data = mkr_1_param[2]
                    mkr1_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr1Colour, symbolBrush=None, name='Mkr 1')
                    OSNR_mkr_1_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_1_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_1_plot_center = self.p1.plot(x=[], y=[])
        else:
            self.p1.removeItem(mkr1_plot)
            self.p1.removeItem(BW_mkr_1_plot_left)
            self.p1.removeItem(BW_mkr_1_plot_right)
            self.p1.removeItem(BW_mkr_1_plot_centre)
            self.p1.removeItem(noise_mkr_1_plot)
            self.p1.removeItem(delta_mkr_1_plot)
            self.p1.removeItem(OSNR_mkr_1_plot_left)
            self.p1.removeItem(OSNR_mkr_1_plot_right)
            self.p1.removeItem(OSNR_mkr_1_plot_centre)
            mkr1_plot = self.p1.plot(x=[], y=[])
            BW_mkr_1_plot_left = self.p1.plot(x=[], y=[])
            BW_mkr_1_plot_right = self.p1.plot(x=[], y=[])
            BW_mkr_1_plot_center = self.p1.plot(x=[], y=[])
            noise_mkr_1_plot = self.p1.plot(x=[], y=[])
            delta_mkr_1_plot = self.p1.plot(x=[], y=[])
            OSNR_mkr_1_plot_left = self.p1.plot(x=[], y=[])
            OSNR_mkr_1_plot_right = self.p1.plot(x=[], y=[])
            OSNR_mkr_1_plot_centre = self.p1.plot(x=[], y=[])

        if mkr_2_param[0] == '1' and viewMkr2 == 1:
            if mkr_2_param[3] == 'ON':
                self.p1.removeItem(mkr2_plot)
                self.p1.removeItem(BW_mkr_2_plot_left)
                self.p1.removeItem(BW_mkr_2_plot_right)
                self.p1.removeItem(BW_mkr_2_plot_centre)
                BW_mkr_2_plot_left = self.p1.plot([self.convertUnits(BW_2_param[0], 'BW', BW_units)], [BW_2_param[3]], symbol='o', symbolPen=mkr2Colour, symbolBrush=None, name='BW Mkr 2 Left')
                BW_mkr_2_plot_right = self.p1.plot([self.convertUnits(BW_2_param[1], 'BW', BW_units)], [BW_2_param[4]], symbol='o', symbolPen=mkr2Colour, symbolBrush=None, name='BW Mkr 2 Right')
                BW_mkr_2_plot_centre = self.p1.plot([self.convertUnits(mkr_2_param[1], 'BW', BW_units)], [mkr_2_param[2]], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='BW Mkr 2 Centre')
            elif mkr_2_param[3] == 'OFF':     
                self.p1.removeItem(mkr2_plot)
                self.p1.removeItem(BW_mkr_2_plot_left)
                self.p1.removeItem(BW_mkr_2_plot_right)
                self.p1.removeItem(BW_mkr_2_plot_centre)
                x_data = self.convertUnits(mkr_2_param[1], 'mkr', mkr_units)
                y_data = mkr_2_param[2]
                mkr2_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='Mkr 2')
                BW_mkr_2_plot_left = self.p1.plot(x=[], y=[])
                BW_mkr_2_plot_right = self.p1.plot(x=[], y=[])
                BW_mkr_2_plot_centre = self.p1.plot(x=[], y=[])
            if mkr_2_param[4] == 'ON':
                self.p1.removeItem(mkr2_plot)
                self.p1.removeItem(noise_mkr_2_plot)
                x_data = self.convertUnits(mkr_2_param[1], 'mkr', mkr_units)
                y_data = mkr_2_param[2]
                noise_mkr_2_plot = self.p1.plot([x_data], [y_data], symbol='s', symbolPen=mkr2Colour, symbolBrush=None, name='Noise Mkr 2')
            elif mkr_2_param[4] == 'OFF':
                if mkr_2_param[3] == 'ON':
                    self.p1.removeItem(noise_mkr_2_plot)
                    noise_mkr_2_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr2_plot)
                    self.p1.removeItem(noise_mkr_2_plot)
                    x_data = self.convertUnits(mkr_2_param[1], 'mkr', mkr_units)
                    y_data = mkr_2_param[2]
                    mkr2_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='Mkr 2')
                    noise_mkr_2_plot = self.p1.plot(x=[], y=[])
            if mkr_2_param[5] == 'ON':
                self.p1.removeItem(mkr2_plot)
                self.p1.removeItem(delta_mkr_2_plot)
                mkr2_plot = self.p1.plot([self.convertUnits(delta_2_param[2], 'delta', delta_units)], [delta_2_param[3]], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='Mkr 2')
                delta_mkr_2_plot = self.p1.plot([self.convertUnits(delta_2_param[0], 'delta', delta_units)], [delta_2_param[1]], symbol='o', symbolPen=mkr2Colour, symbolBrush=None, name='Delta Mkr 2')
            elif mkr_2_param[5] == 'OFF':
                if mkr_2_param[4] == 'ON' or mkr_2_param[3] == 'ON':
                    self.p1.removeItem(delta_mkr_2_plot)
                    delta_mkr_2_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr2_plot)
                    self.p1.removeItem(delta_mkr_2_plot)
                    x_data = self.convertUnits(mkr_2_param[1], 'mkr', mkr_units)
                    y_data = mkr_2_param[2]
                    mkr2_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='Mkr 2')
                    delta_mkr_2_plot = self.p1.plot(x=[], y=[])
            if mkr_2_param[6] == 'ON':
                self.p1.removeItem(mkr2_plot)
                self.p1.removeItem(OSNR_mkr_2_plot_left)
                self.p1.removeItem(OSNR_mkr_2_plot_right)
                self.p1.removeItem(OSNR_mkr_2_plot_centre)
                mkr2_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='Mkr 2')
                OSNR_mkr_2_plot_left = self.p1.plot([self.convertUnits(OSNR_2_param[0], 'mkr', mkr_units)], [OSNR_2_param[1]], symbol='s', symbolPen=mkr2Colour, symbolBrush=None, name='OSNR Mkr 2 Left')
                OSNR_mkr_2_plot_right = self.p1.plot([self.convertUnits(OSNR_2_param[2], 'mkr', mkr_units)], [OSNR_2_param[3]], symbol='s', symbolPen=mkr2Colour, symbolBrush=None, name='OSNR Mkr 2 Right')
                OSNR_mkr_2_plot_centre = self.p1.plot([self.convertUnits(OSNR_2_param[4], 'mkr', mkr_units)],[OSNR_2_param[5]], symbol='o', symbolPen=mkr2Colour, symbolBrush=None, name='OSNR Mkr 2 Centre')
            elif mkr_2_param[6] == 'OFF':
                if mkr_2_param[5] == 'ON' or mkr_2_param[4] == 'ON' or mkr_2_param[3] == 'ON':
                    self.p1.removeItem(OSNR_mkr_2_plot_left)
                    self.p1.removeItem(OSNR_mkr_2_plot_right)
                    self.p1.removeItem(OSNR_mkr_2_plot_centre)
                    OSNR_mkr_2_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_2_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_2_plot_centre = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr2_plot)
                    self.p1.removeItem(OSNR_mkr_2_plot_left)
                    self.p1.removeItem(OSNR_mkr_2_plot_right)
                    self.p1.removeItem(OSNR_mkr_2_plot_centre)
                    x_data = self.convertUnits(mkr_2_param[1], 'mkr', mkr_units)
                    y_data = mkr_2_param[2]
                    mkr2_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr2Colour, symbolBrush=None, name='Mkr 2')
                    OSNR_mkr_2_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_2_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_2_plot_center = self.p1.plot(x=[], y=[])
        else:
            self.p1.removeItem(mkr2_plot)
            self.p1.removeItem(BW_mkr_2_plot_left)
            self.p1.removeItem(BW_mkr_2_plot_right)
            self.p1.removeItem(BW_mkr_2_plot_centre)
            self.p1.removeItem(noise_mkr_2_plot)
            self.p1.removeItem(delta_mkr_2_plot)
            self.p1.removeItem(OSNR_mkr_2_plot_left)
            self.p1.removeItem(OSNR_mkr_2_plot_right)
            self.p1.removeItem(OSNR_mkr_2_plot_centre)
            mkr2_plot = self.p1.plot(x=[], y=[])
            BW_mkr_2_plot_left = self.p1.plot(x=[], y=[])
            BW_mkr_2_plot_right = self.p1.plot(x=[], y=[])
            BW_mkr_2_plot_center = self.p1.plot(x=[], y=[])
            noise_mkr_2_plot = self.p1.plot(x=[], y=[])
            delta_mkr_2_plot = self.p1.plot(x=[], y=[])
            OSNR_mkr_2_plot_left = self.p1.plot(x=[], y=[])
            OSNR_mkr_2_plot_right = self.p1.plot(x=[], y=[])
            OSNR_mkr_2_plot_centre = self.p1.plot(x=[], y=[])
 
        if mkr_3_param[0] == '1' and viewMkr3 == 1:
            if mkr_3_param[3] == 'ON':
                self.p1.removeItem(mkr3_plot)
                self.p1.removeItem(BW_mkr_3_plot_left)
                self.p1.removeItem(BW_mkr_3_plot_right)
                self.p1.removeItem(BW_mkr_3_plot_centre)
                BW_mkr_3_plot_left = self.p1.plot([self.convertUnits(BW_3_param[0], 'BW', BW_units)], [BW_3_param[3]], symbol='o', symbolPen=mkr3Colour, symbolBrush=None, name='BW mkr 3 Left')
                BW_mkr_3_plot_right = self.p1.plot([self.convertUnits(BW_3_param[1], 'BW', BW_units)], [BW_3_param[4]], symbol='o', symbolPen=mkr3Colour, symbolBrush=None, name='BW mkr 3 Right')
                BW_mkr_3_plot_centre = self.p1.plot([self.convertUnits(mkr_3_param[1], 'BW', BW_units)], [mkr_3_param[2]], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='BW mkr 3 Centre')
            elif mkr_3_param[3] == 'OFF':     
                self.p1.removeItem(mkr3_plot)
                self.p1.removeItem(BW_mkr_3_plot_left)
                self.p1.removeItem(BW_mkr_3_plot_right)
                self.p1.removeItem(BW_mkr_3_plot_centre)
                x_data = self.convertUnits(mkr_3_param[1], 'mkr', mkr_units)
                y_data = mkr_3_param[2]
                mkr3_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='mkr 3')
                BW_mkr_3_plot_left = self.p1.plot(x=[], y=[])
                BW_mkr_3_plot_right = self.p1.plot(x=[], y=[])
                BW_mkr_3_plot_centre = self.p1.plot(x=[], y=[])
            if mkr_3_param[4] == 'ON':
                self.p1.removeItem(mkr3_plot)
                self.p1.removeItem(noise_mkr_3_plot)
                x_data = self.convertUnits(mkr_3_param[1], 'mkr', mkr_units)
                y_data = mkr_3_param[2]
                noise_mkr_3_plot = self.p1.plot([x_data], [y_data], symbol='s', symbolPen=mkr3Colour, symbolBrush=None, name='Noise mkr 3')
            elif mkr_3_param[4] == 'OFF':
                if mkr_3_param[3] == 'ON':
                    self.p1.removeItem(noise_mkr_3_plot)
                    noise_mkr_3_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr3_plot)
                    self.p1.removeItem(noise_mkr_3_plot)
                    x_data = self.convertUnits(mkr_3_param[1], 'mkr', mkr_units)
                    y_data = mkr_3_param[2]
                    mkr3_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='mkr 3')
                    noise_mkr_3_plot = self.p1.plot(x=[], y=[])
            if mkr_3_param[5] == 'ON':
                self.p1.removeItem(mkr3_plot)
                self.p1.removeItem(delta_mkr_3_plot)
                mkr3_plot = self.p1.plot([self.convertUnits(delta_3_param[2], 'delta', delta_units)], [delta_3_param[3]], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='mkr 3')
                delta_mkr_3_plot = self.p1.plot([self.convertUnits(delta_3_param[0], 'delta', delta_units)], [delta_3_param[1]], symbol='o', symbolPen=mkr3Colour, symbolBrush=None, name='Delta mkr 3')
            elif mkr_3_param[5] == 'OFF':
                if mkr_3_param[4] == 'ON' or mkr_3_param[3] == 'ON':
                    self.p1.removeItem(delta_mkr_3_plot)
                    delta_mkr_3_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr3_plot)
                    self.p1.removeItem(delta_mkr_3_plot)
                    x_data = self.convertUnits(mkr_3_param[1], 'mkr', mkr_units)
                    y_data = mkr_3_param[2]
                    mkr3_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='mkr 3')
                    delta_mkr_3_plot = self.p1.plot(x=[], y=[])
            if mkr_3_param[6] == 'ON':
                self.p1.removeItem(mkr3_plot)
                self.p1.removeItem(OSNR_mkr_3_plot_left)
                self.p1.removeItem(OSNR_mkr_3_plot_right)
                self.p1.removeItem(OSNR_mkr_3_plot_centre)
                mkr3_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='mkr 3')
                OSNR_mkr_3_plot_left = self.p1.plot([self.convertUnits(OSNR_3_param[0], 'mkr', mkr_units)], [OSNR_3_param[1]], symbol='s', symbolPen=mkr3Colour, symbolBrush=None, name='OSNR mkr 3 Left')
                OSNR_mkr_3_plot_right = self.p1.plot([self.convertUnits(OSNR_3_param[2], 'mkr', mkr_units)], [OSNR_3_param[3]], symbol='s', symbolPen=mkr3Colour, symbolBrush=None, name='OSNR mkr 3 Right')
                OSNR_mkr_3_plot_centre = self.p1.plot([self.convertUnits(OSNR_3_param[4], 'mkr', mkr_units)],[OSNR_3_param[5]], symbol='o', symbolPen=mkr3Colour, symbolBrush=None, name='OSNR mkr 3 Centre')
            elif mkr_3_param[6] == 'OFF':
                if mkr_3_param[5] == 'ON' or mkr_3_param[4] == 'ON' or mkr_3_param[3] == 'ON':
                    self.p1.removeItem(OSNR_mkr_3_plot_left)
                    self.p1.removeItem(OSNR_mkr_3_plot_right)
                    self.p1.removeItem(OSNR_mkr_3_plot_centre)
                    OSNR_mkr_3_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_3_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_3_plot_centre = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr3_plot)
                    self.p1.removeItem(OSNR_mkr_3_plot_left)
                    self.p1.removeItem(OSNR_mkr_3_plot_right)
                    self.p1.removeItem(OSNR_mkr_3_plot_centre)
                    x_data = self.convertUnits(mkr_3_param[1], 'mkr', mkr_units)
                    y_data = mkr_3_param[2]
                    mkr3_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr3Colour, symbolBrush=None, name='mkr 3')
                    OSNR_mkr_3_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_3_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_3_plot_center = self.p1.plot(x=[], y=[])
        else:
            self.p1.removeItem(mkr3_plot)
            self.p1.removeItem(BW_mkr_3_plot_left)
            self.p1.removeItem(BW_mkr_3_plot_right)
            self.p1.removeItem(BW_mkr_3_plot_centre)
            self.p1.removeItem(noise_mkr_3_plot)
            self.p1.removeItem(delta_mkr_3_plot)
            self.p1.removeItem(OSNR_mkr_3_plot_left)
            self.p1.removeItem(OSNR_mkr_3_plot_right)
            self.p1.removeItem(OSNR_mkr_3_plot_centre)
            mkr3_plot = self.p1.plot(x=[], y=[])
            BW_mkr_3_plot_left = self.p1.plot(x=[], y=[])
            BW_mkr_3_plot_right = self.p1.plot(x=[], y=[])
            BW_mkr_3_plot_center = self.p1.plot(x=[], y=[])
            noise_mkr_3_plot = self.p1.plot(x=[], y=[])
            delta_mkr_3_plot = self.p1.plot(x=[], y=[])
            OSNR_mkr_3_plot_left = self.p1.plot(x=[], y=[])
            OSNR_mkr_3_plot_right = self.p1.plot(x=[], y=[])
            OSNR_mkr_3_plot_centre = self.p1.plot(x=[], y=[])
            
        if mkr_4_param[0] == '1' and viewMkr4 == 1:
            if mkr_4_param[3] == 'ON':
                self.p1.removeItem(mkr4_plot)
                self.p1.removeItem(BW_mkr_4_plot_left)
                self.p1.removeItem(BW_mkr_4_plot_right)
                self.p1.removeItem(BW_mkr_4_plot_centre)
                BW_mkr_4_plot_left = self.p1.plot([self.convertUnits(BW_4_param[0], 'BW', BW_units)], [BW_4_param[3]], symbol='o', symbolPen=mkr4Colour, symbolBrush=None, name='BW mkr 4 Left')
                BW_mkr_4_plot_right = self.p1.plot([self.convertUnits(BW_4_param[1], 'BW', BW_units)], [BW_4_param[4]], symbol='o', symbolPen=mkr4Colour, symbolBrush=None, name='BW mkr 4 Right')
                BW_mkr_4_plot_centre = self.p1.plot([self.convertUnits(mkr_4_param[1], 'BW', BW_units)], [mkr_4_param[2]], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='BW mkr 4 Centre')
            elif mkr_4_param[3] == 'OFF':     
                self.p1.removeItem(mkr4_plot)
                self.p1.removeItem(BW_mkr_4_plot_left)
                self.p1.removeItem(BW_mkr_4_plot_right)
                self.p1.removeItem(BW_mkr_4_plot_centre)
                x_data = self.convertUnits(mkr_4_param[1], 'mkr', mkr_units)
                y_data = mkr_4_param[2]
                mkr4_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='mkr 4')
                BW_mkr_4_plot_left = self.p1.plot(x=[], y=[])
                BW_mkr_4_plot_right = self.p1.plot(x=[], y=[])
                BW_mkr_4_plot_centre = self.p1.plot(x=[], y=[])
            if mkr_4_param[4] == 'ON':
                self.p1.removeItem(mkr4_plot)
                self.p1.removeItem(noise_mkr_4_plot)
                x_data = self.convertUnits(mkr_4_param[1], 'mkr', mkr_units)
                y_data = mkr_4_param[2]
                noise_mkr_4_plot = self.p1.plot([x_data], [y_data], symbol='s', symbolPen=mkr4Colour, symbolBrush=None, name='Noise mkr 4')
            elif mkr_4_param[4] == 'OFF':
                if mkr_4_param[3] == 'ON':
                    self.p1.removeItem(noise_mkr_4_plot)
                    noise_mkr_4_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr4_plot)
                    self.p1.removeItem(noise_mkr_4_plot)
                    x_data = self.convertUnits(mkr_4_param[1], 'mkr', mkr_units)
                    y_data = mkr_4_param[2]
                    mkr4_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='mkr 4')
                    noise_mkr_4_plot = self.p1.plot(x=[], y=[])
            if mkr_4_param[5] == 'ON':
                self.p1.removeItem(mkr4_plot)
                self.p1.removeItem(delta_mkr_4_plot)
                mkr4_plot = self.p1.plot([self.convertUnits(delta_4_param[2], 'delta', delta_units)], [delta_4_param[3]], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='mkr 4')
                delta_mkr_4_plot = self.p1.plot([self.convertUnits(delta_4_param[0], 'delta', delta_units)], [delta_4_param[1]], symbol='o', symbolPen=mkr4Colour, symbolBrush=None, name='Delta mkr 4')
            elif mkr_4_param[5] == 'OFF':
                if mkr_4_param[4] == 'ON' or mkr_4_param[3] == 'ON':
                    self.p1.removeItem(delta_mkr_4_plot)
                    delta_mkr_4_plot = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr4_plot)
                    self.p1.removeItem(delta_mkr_4_plot)
                    x_data = self.convertUnits(mkr_4_param[1], 'mkr', mkr_units)
                    y_data = mkr_4_param[2]
                    mkr4_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='mkr 4')
                    delta_mkr_4_plot = self.p1.plot(x=[], y=[])
            if mkr_4_param[6] == 'ON':
                self.p1.removeItem(mkr4_plot)
                self.p1.removeItem(OSNR_mkr_4_plot_left)
                self.p1.removeItem(OSNR_mkr_4_plot_right)
                self.p1.removeItem(OSNR_mkr_4_plot_centre)
                mkr4_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='mkr 4')
                OSNR_mkr_4_plot_left = self.p1.plot([self.convertUnits(OSNR_4_param[0], 'mkr', mkr_units)], [OSNR_4_param[1]], symbol='s', symbolPen=mkr4Colour, symbolBrush=None, name='OSNR mkr 4 Left')
                OSNR_mkr_4_plot_right = self.p1.plot([self.convertUnits(OSNR_4_param[2], 'mkr', mkr_units)], [OSNR_4_param[3]], symbol='s', symbolPen=mkr4Colour, symbolBrush=None, name='OSNR mkr 4 Right')
                OSNR_mkr_4_plot_centre = self.p1.plot([self.convertUnits(OSNR_4_param[4], 'mkr', mkr_units)],[OSNR_4_param[5]], symbol='o', symbolPen=mkr4Colour, symbolBrush=None, name='OSNR mkr 4 Centre')
            elif mkr_4_param[6] == 'OFF':
                if mkr_4_param[5] == 'ON' or mkr_4_param[4] == 'ON' or mkr_4_param[3] == 'ON':
                    self.p1.removeItem(OSNR_mkr_4_plot_left)
                    self.p1.removeItem(OSNR_mkr_4_plot_right)
                    self.p1.removeItem(OSNR_mkr_4_plot_centre)
                    OSNR_mkr_4_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_4_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_4_plot_centre = self.p1.plot(x=[], y=[])
                else:
                    self.p1.removeItem(mkr4_plot)
                    self.p1.removeItem(OSNR_mkr_4_plot_left)
                    self.p1.removeItem(OSNR_mkr_4_plot_right)
                    self.p1.removeItem(OSNR_mkr_4_plot_centre)
                    x_data = self.convertUnits(mkr_4_param[1], 'mkr', mkr_units)
                    y_data = mkr_4_param[2]
                    mkr4_plot = self.p1.plot([x_data], [y_data], symbol='d', symbolPen=mkr4Colour, symbolBrush=None, name='mkr 4')
                    OSNR_mkr_4_plot_left = self.p1.plot(x=[], y=[])
                    OSNR_mkr_4_plot_right = self.p1.plot(x=[], y=[])
                    OSNR_mkr_4_plot_center = self.p1.plot(x=[], y=[])
        else:
            self.p1.removeItem(mkr4_plot)
            self.p1.removeItem(BW_mkr_4_plot_left)
            self.p1.removeItem(BW_mkr_4_plot_right)
            self.p1.removeItem(BW_mkr_4_plot_centre)
            self.p1.removeItem(noise_mkr_4_plot)
            self.p1.removeItem(delta_mkr_4_plot)
            self.p1.removeItem(OSNR_mkr_4_plot_left)
            self.p1.removeItem(OSNR_mkr_4_plot_right)
            self.p1.removeItem(OSNR_mkr_4_plot_centre)
            mkr4_plot = self.p1.plot(x=[], y=[])
            BW_mkr_4_plot_left = self.p1.plot(x=[], y=[])
            BW_mkr_4_plot_right = self.p1.plot(x=[], y=[])
            BW_mkr_4_plot_center = self.p1.plot(x=[], y=[])
            noise_mkr_4_plot = self.p1.plot(x=[], y=[])
            delta_mkr_4_plot = self.p1.plot(x=[], y=[])
            OSNR_mkr_4_plot_left = self.p1.plot(x=[], y=[])
            OSNR_mkr_4_plot_right = self.p1.plot(x=[], y=[])
            OSNR_mkr_4_plot_centre = self.p1.plot(x=[], y=[])

    # This is the main function which plots the different traces on the display
    def traceDisplay(self, num_points, active_trace, xLabel, yLabel, xUnits, yUnits, trace_a_data, trace_b_data, trace_c_data,
                trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param, trace_d_param, trace_e_param, trace_f_param,
                     sweep):
        global trace_start
        global trace_stop
        global TRA_plot
        global TRB_plot
        global TRC_plot
        global TRD_plot
        global TRE_plot
        global TRF_plot
        global traceA
        global traceB
        global traceC
        global traceD
        global traceE
        global traceF
        global trace_x_values
        global trace_y_values
        global frame_start
        global frame_stop
        
        self.p1.clear()
        self.p1.setLabel('left', '%s' %yLabel, units='%s' %yUnits)
        self.p1.setLabel('bottom', '%s' %xLabel, units='%s' %xUnits)
        trace_start = 0
        trace_stop = 0

        if sweep == 1:
            instrument1.write("INIT:CONT OFF")
            instrument1.write("INIT:IMM;*OPC?") # Take a sweep and wait for finish
            
        if trace_a_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRA")) # finds start of trace in right format 
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRA")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRA")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceA = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            if min(trace_y_values) < -250:
                self.plotException()
                TRA_plot = self.p1.plot(x=[], y=[])
            else:
                TRA_plot = self.p1.plot(traceA, pen='y', name='Trace A')
            
        if trace_b_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRB")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRB")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRB")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceB = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            if min(trace_y_values) < -250:
                self.plotException()
                TRB_plot = self.p1.plot(x=[], y=[])
            else:
                TRB_plot = self.p1.plot(traceB, pen='g', name='Trace B')
            

        if trace_c_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRC")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRc")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRC")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceC = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            if min(trace_y_values) < -250:
                self.plotException()
                TRC_plot = self.p1.plot(x=[], y=[])
            else:
                TRC_plot = self.p1.plot(traceC, pen='c', name='Trace C')
            
        if trace_d_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRD")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRD")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRD")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceD = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            if min(trace_y_values) < -250:
                self.plotException()
                TRD_plot = self.p1.plot(x=[], y=[])
            else:
                TRD_plot = self.p1.plot(traceD, pen='r', name='Trace D')
            
        if trace_e_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRE")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRE")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRE")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceE = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            if min(trace_y_values) < -250:
                self.plotException()
                TRE_plot = self.p1.plot(x=[], y=[])
            else:
                TRE_plot = self.p1.plot(traceE, pen='b', name='Trace E')
            
        if trace_f_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRF")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRF")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRF")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceF = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            if min(trace_y_values) < -250:
                self.plotException()
                TRF_plot = self.p1.plot(x=[], y=[])
            else:
                TRF_plot = self.p1.plot(traceF, pen='m', name='Trace F')

        frame_start = ast.literal_eval(instrument1.query("SENSe:WAVelength:STARt?")) # finds left hand side of display
        frame_stop = ast.literal_eval(instrument1.query("SENSe:WAVelength:STOP?")) # finds right hand side of display

        # Plotting the reference level
        global ref_level
        global ref_plot
        self.p1.removeItem(ref_plot)
        ref_level = instrument1.query("DISPlay:WINDow:TRACe:Y:SCALe:RLEVel?")
        ref_level = conversions.str2float(ref_level,"dBm")
        x_ref = numpy.linspace(frame_start,frame_stop,int(num_points))
        y_ref = numpy.ones(int(num_points))
        y_ref = ref_level*y_ref
        ref_plot = self.p1.plot(x_ref, y_ref, pen='g', name='Ref Level')
        self.p1.setXRange(frame_start,frame_stop)
        self.graphLayout.addWidget(self.p1)

    def contPlot(self):
        global TRA_plot
        global TRB_plot
        global TRC_plot
        global TRD_plot
        global TRE_plot
        global TRF_plot
        global traceA
        global traceB
        global traceC
        global traceD
        global traceE
        global traceF
        global ref_level
        global ref_plot
        global x_ref
        global y_ref
        global resetGraph

        self.p1.clear()
        self.p1.setLabel('left', '%s' %amplitude_name, units='%s' %amplitude_units)
        self.p1.setLabel('bottom', '%s' %wavelength_name, units='%s' %wavelength_units_display)

        if trace_a_param[1] == "ON":
            if min(traceA[:,1]) > -250:
                TRA_plot = self.p1.plot(traceA, pen='y', name='Trace A')

        if trace_b_param[1] == "ON":
            if min(traceB[:,1]) > -250:
                TRB_plot = self.p1.plot(traceB, pen='g', name='Trace B')

        if trace_c_param[1] == "ON":
            if min(traceC[:,1]) > -250:
                TRC_plot = self.p1.plot(traceC, pen='c', name='Trace C')

        if trace_d_param[1] == "ON":
            if min(traceD[:,1]) > -250:
                TRD_plot = self.p1.plot(traceD, pen='r', name='Trace D')
            
        if trace_e_param[1] == "ON":
            if min(traceE[:,1]) > -250:
                TRE_plot = self.p1.plot(traceE, pen='b', name='Trace E')

        if trace_f_param[1] == "ON":
            if min(traceF[:,1]) > -250:
                TRF_plot = self.p1.plot(traceF, pen='m', name='Trace F')

        self.p1.removeItem(ref_plot)
        ref_plot = self.p1.plot(x_ref, y_ref, pen='g', name='Ref Level')

        if resetGraph == 1:
            self.p1.setXRange(frame_start,frame_stop)
            resetGraph = resetGraph + 1

        if active_marker == '1':
            self.mkr1ContDisplay()
        elif active_marker == '2':
            self.mkr2ContDisplay()
        elif active_marker == '3':
            self.mkr3ContDisplay()
        elif active_marker == '4':
            self.mkr4ContDisplay()

        if lineMarkerOnOff == 'On' or traceIntOnOff == "ON":
            self.linemarkerPlot()
            self.btmLabel61.setText("%0.2f dBm" %integValue)
        else:
            self.btmLabel61.setText("")

        self.markerPlot()

    def contPlotStop(self):
        global reset
        self.contSweep.terminate()
        reset = 0
        
    # Function to plot the line markers defined in the line markers menu
    def linemarkerPlot(self):
        global line_1_plot
        global line_2_plot
        global line1
        global line2
        global lineMarkerOnOff
        if lineMarkerOnOff == 'On':
            x_line_1 = float(line1)*0.000000001
            x_line_2 = float(line2)*0.000000001
            y_range = self.p1.viewRange()
            y_range = y_range[1]
            y_upper = y_range[1]
            y_lower = y_range[0]
            y_values = numpy.linspace(y_lower,y_upper,10000)
            x_values = numpy.ones(10000)
            x1 = x_values*x_line_1
            x2 = x_values*x_line_2
            self.p1.removeItem(line_1_plot)
            self.p1.removeItem(line_2_plot)
            line_1_plot = self.p1.plot(x1, y_values, pen='y', name='Line Marker 1')
            line_2_plot = self.p1.plot(x2, y_values, pen='y', name='Line Marker 2')
        elif lineMarkerOnOff == 'Off':
            self.p1.removeItem(line_1_plot)
            self.p1.removeItem(line_2_plot)
            line_1_plot = self.p1.plot(x=[], y=[])
            line_2_plot = self.p1.plot(x=[], y=[])

    # Function to plot the user threshold defined in the marker setup menu
    def threshPlot(self):
        global mkrThreshOnOff
        global userMkrThresh
        global trace_start
        global trace_stop
        global thresh_plot
        if mkrThreshOnOff == 'ON':
            self.p1.removeItem(thresh_plot)
            thresh_level = userMkrThresh
            x_thresh = numpy.linspace(trace_start,trace_stop,10000)
            y_thresh = numpy.ones(10000)
            y_thresh = y_thresh*float(thresh_level)
            thresh_plot = self.p1.plot(x_thresh, y_thresh, pen='c', name='Threshold')
        elif mkrThreshOnOff == 'OFF':
            self.p1.removeItem(thresh_plot)
            thresh_plot = self.p1.plot(x=[], y=[])


## ------------------------------------------------------
##          SETUP FUNCTIONS
## ------------------------------------------------------
    # Setup instrument is run at start up of the OSA to query the machine and determines initial values and settings
    def setupInstrument(self): 
        global menuFlag
        menuFlag = ''
    
        global active_marker
        global active_trace
        global active_trace_num

        global indent_margin
        indent_margin = 5
        
        global wavelength_units
        wavelength_units = "nm" 
        
        global wavelength_units_display
        if wavelength_units == 'nm' or wavelength_units == 'um':
            wavelength_units_display = 'm'
        elif wavelength_units == 'Ang':
            wavelength_units_display = 'Ang'
        else:
            wavelength_units_display = 'm'

        global logLin
        logLin = str(instrument1.query("DISPlay:WINDow:TRACe:Y:SCALe:SPACing?")).rstrip()

        global amplitude_units 
        if logLin == 'LOG':
            amplitude_units = 'dB'
        elif logLin == 'LIN':
            amplitude_units  = 'W'

        global time_units
        time_units = 'us'

        global frequency_units
        frequency_units = 'kHz'

        global autoMan
        autoMan = str(instrument1.query("SENSe:POWer:DC:RANGe:LOWer:AUTO?")).rstrip()
        if autoMan == "1":
            autoMan = "AUTO"
        elif autoMan == "0":
            autoMan = "MAN"

        global traceIntOnOff
        traceIntOnOff = str(instrument1.query("CALCulate:TPOWer:STATe?")).rstrip()
        if traceIntOnOff == "1":
            traceIntOnOff = "ON"
        elif traceIntOnOff == "0":
            traceIntOnOff = "OFF"

        global peakPit
        peakPit = "PEAK"

        global upDown
        upDown = "Down"

        global search_flag
        search_flag = instrument1.query("CALCulate:MARKer:SRANge:STATe?")
        if search_flag == '1':
            search_flag = 1
        else:
            search_flag = 0

        global sweep_flag
        sweep_flag = instrument1.query("SENSe:WAVelength:SRANge:STATe?")
        if sweep_flag == '1':
            sweep_flag = 1
        else:
            sweep_flag = 0

        global sweep_limit
        sweep_limit = str(instrument1.query("SENSe:WAVelength:SRANge:STATe?")).rstrip()
        if sweep_limit == '0':
            sweep_limit = 'Off'
        else:
            sweep_limit = 'On'

        global search_limit
        search_limit = str(instrument1.query("CALCulate:MARKer:SRANge:STATe?")).rstrip()
        if search_limit == '0':
            search_limit = 'Off'
        else:
            search_limit = 'On'

        global integral_limit
        integral_limit = str(instrument1.query("CALCulate:TPOWer:IRANge:STATe?")).rstrip()
        if integral_limit == '0':
            integral_limit = 'Off'
        else:
            integral_limit = 'On'

        global trace_integral
        trace_integral = str(instrument1.query("CALCulate:TPOWer:STATe?")).rstrip()
        if trace_integral == '0':
            trace_integral = 'Off'
        else:
            trace_integral = 'On'

        global line1
        line1 = str(instrument1.query("CALCulate:TPOWer:IRANge:LOWer?")).rstrip()
        line1 = str(conversions.str2float(line1, wavelength_units))

        global line2
        line2 = str(instrument1.query("CALCulate:TPOWer:IRANge:UPPer?")).rstrip()
        line2 = str(conversions.str2float(line2, wavelength_units))

        global mkr_units
        mkr_units = 'nm'

        global BW_units
        BW_units = 'nm'

        global delta_units
        delta_units = 'nm'

        global mkrInterpOnOff
        mkrInterpOnOff = str(instrument1.query("CALCulate:MARKer:INT?")).rstrip()
        if mkrInterpOnOff == '0':
            mkrInterpOnOff = 'OFF'
        elif mkrInterpOnOff == '1':
            mkrInterpOnOff = 'ON'

        global BWInterpOnOff
        BWInterpOnOff = str(instrument1.query("CALCulate:MARKer:FUNCtion:BANDwidth:INT?")).rstrip()
        if BWInterpOnOff == '0':
            BWInterpOnOff = 'OFF'
        elif BWInterpOnOff == '1':
            BWInterpOnOff = 'ON'

        global mkrThreshOnOff
        mkrThreshOnOff = str(instrument1.query("CALCulate:THReshold:STATe?")).rstrip()
        if mkrThreshOnOff == '0':
            mkrThreshOnOff = 'OFF'
        elif mkrThreshOnOff == '1':
            mkrThreshOnOff = 'ON'

        global userMkrThresh
        if mkrThreshOnOff == 'ON':
            userMkrThresh = str(instrument1.query("CALCulate:THReshold?")).rstrip()
            userMkrThresh = str(conversions.str2float(userMkrThresh,'dB'))
        else:
            userMkrThresh = '0'

        global noiseMkrBW
        noiseMkrBW = str(instrument1.query("CALCulate:MARKer:FUNCtion:NOISe:BANDwidth?")).rstrip()
        noiseMkrBW = str(conversions.str2float(noiseMkrBW,'nm'))

        global OSNRType
        OSNRType = str(instrument1.query("CALCulate:MARKer:FUNCtion:OSNR:MODE?")).rstrip()

        global OSNROffset
        if OSNRType == 'MAN':
            OSNROffset = str(instrument1.query("CALCulate:MARKer:FUNCtion:OSNR:OFFSet?")).rstrip()
        else:
            OSNROffset = '0'

        global peakExcur
        peakExcur = str(instrument1.query("CALCulate:MARKer:PEXCursion:PEAK?")).rstrip()

        global pitExcur
        pitExcur = str(instrument1.query("CALCulate:MARKer:PEXCursion:PIT?")).rstrip()

        global resBw
        value = instrument1.query("SENSe:BANDwidth:RESolution?")
        resBw = conversions.str2float(value,"%s" %wavelength_units)

        global vidBw
        value = instrument1.query("SENSe:BANDwidth:VIDeo?")
        vidBw = conversions.str2float(value,"%s" %frequency_units)

        global sensitivity
        value = str(instrument1.query("SENSe:POWer:DC:RANGe:LOWer?"))
        sensitivity = float(value)

        global sweepTime
        value = instrument1.query("SENSe:SWEep:TIME?")
        sweepTime = float(value)

        global lineMarkerOnOff
        lineMarkerOnOff = str(instrument1.query("CALCulate:TPOWer:IRANge:STATe?").rstrip())
        if lineMarkerOnOff == '1':
            lineMarkerOnOff = 'On'
        elif lineMarkerOnOff == '0':
            lineMarkerOnOff = 'Off'

        global resBwManAuto
        resBwManAuto = str(instrument1.query("SENSe:BANDwidth:RESolution:AUTO?")).rstrip()
        if resBwManAuto == "1":
            resBwManAuto = "AUTO"
        elif resBwManAuto == "0":
            resBwManAuto = "MAN"

        global vidBwManAuto
        vidBwManAuto = str(instrument1.query("SENSe:BANDwidth:VIDeo:AUTO?")).rstrip()
        if vidBwManAuto == "1":
            vidBwManAuto = "AUTO"
        elif vidBwManAuto == "0":
            vidBwManAuto = "MAN"

        global sweepTimeManAuto
        sweepTimeManAuto = str(instrument1.query("SENSe:SWEep:TIME:AUTO?")).rstrip()
        if sweepTimeManAuto == "1":
            sweepTimeManAuto = "AUTO"
        elif sweepTimeManAuto == "0":
            sweepTimeManAuto = "MAN"

        global repeatSweepOnOff
        instrument1.write("INITiate:CONTinuous OFF")
        repeatSweepOnOff = "OFF"

        global trigSyncLowHighPulse
        trigSyncLowHighPulse = str(instrument1.query("TRIGger:OUTPut?")).rstrip()
        if trigSyncLowHighPulse == "ON":
            trigSyncLowHighPulse = "HIGH"
        elif trigSyncLowHighPulse == "OFF":
            trigSyncLowHighPulse = "LOW"
        elif trigSyncLowHighPulse == "AUTO":
            trigSyncLowHighPulse = "PULSE"

        global syncOutOnOff
        syncOutOnOff = str(instrument1.query("TRIGger:OUTPut:PULSe:STATe?")).rstrip()
        if syncOutOnOff == "1":
            syncOutOnOff = "ON"
        elif syncOutOnOff == "0":
            syncOutOnOff = "OFF"

        global wavelengthOffset
        wavelengthOffset = str(ast.literal_eval(instrument1.query("SENSe:WAVelength:OFFSet?")))
        wavelengthOffset = str(conversions.str2float(wavelengthOffset, '%s' %wavelength_units))
        
        global wavelengthStepSize
        wavelengthStepSize = str(instrument1.query("SENse:WAVelength:CENTer:STEP:INCRement?"))
        wavelengthStepSize = str(conversions.str2float(wavelengthStepSize, "%s" %wavelength_units))

        global wavelengthRefIn
        wavelengthRefIn = str(instrument1.query("SENSe:CORRection:RVELocity:MEDium?")).rstrip()

        global num_points
        num_points = str(instrument1.query("SENSe:SWEep:POINts?")).rstrip()

        global Trigger_Mode
        Trigger_Mode = str(instrument1.query("TRIGger:SOURce?")).rstrip()
        if Trigger_Mode == "INT":
            Trigger_Mode = str(instrument1.query("TRIGger:SLOPe?")).rstrip()
            if Trigger_Mode == "POS":
                Trigger_Mode = "ADC+"
            elif Trigger_Mode == "NEG":
                Trigger_Mode = "ADC-"
            elif Trigger_Mode == "EITH":
                Trigger_Mode = "ADC AC"
        elif Trigger_Mode == "IMM":
            Trigger_Mode = "Internal"
        else:
            Trigger_Mode = "External"

        global Power_Calibration
        Power_Calibration = str(instrument1.query("CALibration:POWer:STATe?")).rstrip()

        global auto_ranging
        auto_ranging = str(ast.literal_eval(instrument1.query("SENSe:POWer:DC:RANGe:AUTO?")))

        global auto_zero
        auto_zero = str(ast.literal_eval(instrument1.query("CALibration:ZERO:AUTO?")))

        global amplitude_correction
        amplitude_correction = str(ast.literal_eval(instrument1.query("SENSe:CORRection:CSET?")))

        global amplitude_correction_mode
        amplitude_correction_mode = str(ast.literal_eval(instrument1.query("SENSe:CORRection:STATe?")))

        global auto_chop
        auto_chop = str(ast.literal_eval(instrument1.query("SENSe:CHOP:STATe?")))

        # Turns all math functions off in start-up
        instrument1.write("CALCulate3:MATH:STATe OFF")
        instrument1.write("CALCulate6:MATH:STATe OFF")

        global inUse
        inUse = 0

        global plotDone
        plotDone = 0

        global reset
        reset = 0

        global displayDisabled
        displayDisabled = str(instrument1.query("DISPlay:WINDow?")).rstrip()
        if displayDisabled == "1":
            displayDisabled = 'ON'
        else:
            displayDisabled = 'OFF'

        global traceA
        traceAx = numpy.linspace(0,1000,1000)
        traceAy = numpy.linspace(-400,-400,1000)
        traceA = numpy.array([traceAx,traceAy]).T

        global traceB
        traceBx = numpy.linspace(0,1000,1000)
        traceBy = numpy.linspace(-400,-400,1000)
        traceB = numpy.array([traceBx,traceBy]).T

        global traceC
        traceCx = numpy.linspace(0,1000,1000)
        traceCy = numpy.linspace(-400,-400,1000)
        traceC = numpy.array([traceCx,traceCy]).T

        global traceD
        traceDx = numpy.linspace(0,1000,1000)
        traceDy = numpy.linspace(-400,-400,1000)
        traceD = numpy.array([traceDx,traceDy]).T

        global traceE
        traceEx = numpy.linspace(0,1000,1000)
        traceEy = numpy.linspace(-400,-400,1000)
        traceE = numpy.array([traceEx,traceEy]).T

        global traceF
        traceFx = numpy.linspace(0,1000,1000)
        traceFy = numpy.linspace(-400,-400,1000)
        traceF = numpy.array([traceFx,traceFy]).T

    # Function to setup markers on start-up and sync
    def setupMarkers(self):
        global active_mkr_param
        global mkrOnOff
        global markerBWOnOff
        global noiseMarkOnOff
        global deltaMarkOnOff
        global osnrMarkOnOff
        global mkrTrc
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param
        global active_BW_param
        global BW_1_param
        global BW_2_param
        global BW_3_param
        global BW_4_param
        global delta_1_param
        global delta_2_param
        global delta_3_param
        global delta_4_param
        global OSNR_1_param
        global OSNR_2_param
        global OSNR_3_param
        global OSNR_4_param
        
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        mkr_1_param = [0, 0, 0, '0', '0', '0', '0', '0']
        mkr_2_param = [0, 0, 0, '0', '0', '0', '0', '0']
        mkr_3_param = [0, 0, 0, '0', '0', '0', '0', '0']
        mkr_4_param = [0, 0, 0, '0', '0', '0', '0', '0']
        ## BW_x_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
        BW_1_param = [0, 0, 0, 0, 0, 0]
        BW_2_param = [0, 0, 0, 0, 0, 0]
        BW_3_param = [0, 0, 0, 0, 0, 0]
        BW_4_param = [0, 0, 0, 0, 0, 0]
        # delta_x_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
        delta_1_param = [0, 0, 0, 0, 0]
        delta_2_param = [0, 0, 0, 0, 0]
        delta_3_param = [0, 0, 0, 0, 0]
        delta_4_param = [0, 0, 0, 0, 0]
        # OSNR_x_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
        OSNR_1_param = [0, 0, 0, 0, 0, 0, 0]
        OSNR_2_param = [0, 0, 0, 0, 0, 0, 0]
        OSNR_3_param = [0, 0, 0, 0, 0, 0, 0]
        OSNR_4_param = [0, 0, 0, 0, 0, 0, 0]
        ## active_mkr_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        active_mkr_param = [0, 0, 0, '0', '0', '0', '0', '0']
        ## active_BW_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
        active_BW_param = [0, 0, 0, 0, 0, 0]

        for i in range(1,5):
            if i == 1:
                itrac = '1'
            if i == 2:
                itrac = '2'
            if i == 3:
                itrac = '3'
            if i == 4:
                itrac = '4'

            mkrOnOff = str(instrument1.query("CALC:MARK%s:STAT?" %itrac)).rstrip()
            mkrTrc = str(instrument1.query("CALCulate:MARKer%s:TRACe?" %itrac)).rstrip()

            if itrac == '1':
                mkr_1_param[0] = mkrOnOff
                mkr_1_param[7] = mkrTrc
                self.mkr1NormCalc()
                self.mkr1NormDisplay()
                my = mkr_1_param[2]
            if itrac == '2':
                mkr_2_param[0] = mkrOnOff
                mkr_2_param[7] = mkrTrc
                self.mkr2NormCalc()
                self.mkr2NormDisplay()
                my = mkr_2_param[2]
            if itrac == '3':
                mkr_3_param[0] = mkrOnOff
                mkr_3_param[7] = mkrTrc
                self.mkr3NormCalc()
                self.mkr3NormDisplay()
                my = mkr_3_param[2]
            if itrac == '4':
                mkr_4_param[0] = mkrOnOff
                mkr_4_param[7] = mkrTrc
                self.mkr4NormCalc()
                self.mkr4NormDisplay()
                my = mkr_4_param[2]

            markerBWOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe?" %itrac)).rstrip()
            if markerBWOnOff == "1":
                markerBWOnOff = "ON"
                xL = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:X:LEFT?" %itrac).rstrip())
                BWxL = conversions.str2float(xL, BW_units)
                xR = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:X:RIGHt?" %itrac).rstrip())
                BWxR = conversions.str2float(xR, BW_units)
                xC = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:X:CENTer?" %itrac).rstrip())
                BWxC = conversions.str2float(xC, BW_units)
                mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:NDB?" %itrac),amplitude_units)                                                        
                BWyL = my + mkrBWY
                BWyR = my + mkrBWY
            elif markerBWOnOff == "0":
                markerBWOnOff = "OFF"
                BWxL = 0
                BWxR = 0
                BWyL = 0
                BWyR = 0
                mkrBWY = 0
                BWxC = 0

            noiseMarkOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:NOISe:STATe?" %itrac)).rstrip()
            if noiseMarkOnOff == "1":
                noiseMarkOnOff = "ON"
            elif noiseMarkOnOff == "0":
                noiseMarkOnOff = "OFF"

            deltaMarkOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:DELTa:STATe?" %itrac)).rstrip()
            if deltaMarkOnOff == "1":
                deltaMarkOnOff = "ON"
                delta_distance = instrument1.query("CALC:MARK%s:FUNC:DELTa:X:OFFset?" %itrac)
                delta_distance = conversions.str2float(delta_distance,wavelength_units)
                markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer%s:X?" %itrac).rstrip()),wavelength_units)
                markerY = float(instrument1.query("CALCulate:MARKer%s:Y?" %itrac))
                markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer%s:FUNC:DELta:X:REF?" %itrac).rstrip()),wavelength_units)
                markerYRef = float(instrument1.query("CALCulate:MARKer%s:FUNC:DELta:Y:REF?" %itrac))   
            elif deltaMarkOnOff == "0":
                deltaMarkOnOff = "OFF"
                markerX = 0
                markerY = 0
                markerXRef = 0
                markerYRef = 0
                delta_distance = 0

            osnrMarkOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:STATe?" %itrac)).rstrip()
            if osnrMarkOnOff == "1":
                osnrMarkOnOff = "ON"
            elif osnrMarkOnOff == "0":
                osnrMarkOnOff = "OFF"
            OSNRxL = 0
            OSNRyL = 0
            OSNRxR = 0
            OSNRyR = 0
            OSNRxC = 0
            OSNRyC = 0
            OSNRVal = 0

            if itrac == '1':
                mkr_1_param[3] = markerBWOnOff
                mkr_1_param[4] = noiseMarkOnOff
                mkr_1_param[5] = deltaMarkOnOff
                mkr_1_param[6] = osnrMarkOnOff
                BW_1_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                delta_1_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                OSNR_1_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]

            if itrac == '2':
                mkr_2_param[3] = markerBWOnOff
                mkr_2_param[4] = noiseMarkOnOff
                mkr_2_param[5] = deltaMarkOnOff
                mkr_2_param[6] = osnrMarkOnOff
                BW_2_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                delta_2_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                OSNR_2_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                
            if itrac == '3':
                mkr_3_param[3] = markerBWOnOff
                mkr_3_param[4] = noiseMarkOnOff
                mkr_3_param[5] = deltaMarkOnOff
                mkr_3_param[6] = osnrMarkOnOff
                BW_3_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                delta_3_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                OSNR_3_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                
            if itrac == '4':
                mkr_4_param[3] = markerBWOnOff
                mkr_4_param[4] = noiseMarkOnOff
                mkr_4_param[5] = deltaMarkOnOff
                mkr_4_param[6] = osnrMarkOnOff
                BW_4_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                delta_4_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                OSNR_4_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]

        global active_marker
        if mkr_1_param[0] == '1':
            active_mkr_param = mkr_1_param
            active_marker = '1'
            if mkr_1_param[4] == 'ON':
                self.mkr1NoiseDisplay()
                self.mkrCompDisplay()
            else:
                self.mkr1NormDisplay()
                self.mkrCompDisplay()
        else:
            active_marker = '1'
            active_mkr_param = mkr_1_param
           
        if mkr_2_param[0] == '1':
            active_mkr_param = mkr_2_param
            active_marker = '2'
            if mkr_2_param[4] == 'ON':
                self.mkr2NoiseDisplay()
                self.mkrCompDisplay()
            else:
                self.mkr2NormDisplay()
                self.mkrCompDisplay()
                
        if mkr_3_param[0] == '1':
            active_mkr_param = mkr_3_param
            active_marker = '3'
            if mkr_3_param[4] == 'ON':
                self.mkr3NoiseDisplay()
                self.mkrCompDisplay()
            else:
                self.mkr3NormDisplay()
                self.mkrCompDisplay()
                
        if mkr_4_param[0] == '1':
            active_mkr_param = mkr_4_param
            active_marker = '4'
            if mkr_4_param[4] == 'ON':
                self.mkr4NoiseDisplay()
                self.mkrCompDisplay()
            else:
                self.mkr4NormDisplay()
                self.mkrCompDisplay()

        if active_marker == '1':
            if mkr_1_param[3] == 'ON':
                self.mkr1BWDisplay()
            elif mkr_1_param[5] == 'ON':
                self.mkr1DeltaDisplay()
            elif mkr_1_param[6] == 'ON':
                if bootup == 1:
                    pass
                else:
                    self.mkr1OSNRDisplay()
        elif active_marker == '2':
            if mkr_2_param[3] == 'ON':
                self.mkr2BWDisplay()
            elif mkr_2_param[5] == 'ON':
                self.mkr2DeltaDisplay()
            elif mkr_2_param[6] == 'ON':
                if bootup == 1:
                    pass
                else:
                    self.mkr2OSNRDisplay()
        elif active_marker == '3':
            if mkr_3_param[3] == 'ON':
                self.mkr3BWDisplay()
            elif mkr_3_param[5] == 'ON':
                self.mkr3DeltaDisplay()
            elif mkr_3_param[6] == 'ON':
                if bootup == 1:
                    pass
                else:
                    self.mkr3OSNRDisplay()
        elif active_marker == '4':
            if mkr_4_param[3] == 'ON':
                self.mkr4BWDisplay()
            elif mkr_4_param[5] == 'ON':
                self.mkr4DeltaDisplay()
            elif mkr_4_param[6] == 'ON':
                if bootup == 1:
                    pass
                else:
                    self.mkr4OSNRDisplay()

    # Function to setup traces on start-up and sync
    def setupTrace(self):
        global updateTraceOnOff
        global viewTraceOnOff
        global holdTraceNoneMinMax
        global averagingOnOff
        global trace_a_param
        global trace_b_param
        global trace_c_param
        global trace_d_param
        global trace_e_param
        global trace_f_param
        global trace_a_data
        global trace_b_data
        global trace_c_data
        global trace_d_data
        global trace_e_data
        global trace_f_data

        for i in range(1,7):
            if i == 1:
                itrac = "TRA"
            if i == 2:
                itrac = "TRB"
            if i == 3:
                itrac = "TRC"
            if i == 4:
                itrac = "TRD"
            if i == 5:
                itrac = "TRE"
            if i == 6:
                itrac = "TRF"
                
            updateTraceOnOff = str(instrument1.query("TRACe:FEED:CONTrol? %s" %itrac)).rstrip()
            if updateTraceOnOff == "ALW":
                updateTraceOnOff = "ON"
            elif updateTraceOnOff == "NEV":
                updateTraceOnOff = "OFF"

            viewTraceOnOff = str(instrument1.query("DISPlay:WINDow:TRACe:STATe? %s" %itrac)).rstrip()
            if viewTraceOnOff == "1":
                viewTraceOnOff = "ON"
            elif viewTraceOnOff == "0":
                viewTraceOnOff = "OFF"

            holdTraceMax = str(instrument1.query("CALCulate%s:MAXimum:STATe?" %i)).rstrip()
            holdTraceMin = str(instrument1.query("CALCulate%s:MINimum:STATe?" %i)).rstrip()
            if holdTraceMax == "1" and holdTraceMin == "0":
                holdTraceNoneMinMax = "MAX"
            elif holdTraceMax == "0" and holdTraceMin == "1":
                holdTraceNoneMinMax = "MIN"
            else:
                holdTraceNoneMinMax = "NONE"

            averagingOnOff = str(instrument1.query("CALCulate%s:AVERage:STATe?" %i)).rstrip()
            if averagingOnOff == "1":
                averagingOnOff = "ON"
            elif averagingOnOff == "0":
                averagingOnOff = "OFF"

            if i == 1:
                trace_a_param = [updateTraceOnOff,viewTraceOnOff,holdTraceNoneMinMax,averagingOnOff]
            if i == 2:
                trace_b_param = [updateTraceOnOff,viewTraceOnOff,holdTraceNoneMinMax,averagingOnOff]
            if i == 3:
                trace_c_param = [updateTraceOnOff,viewTraceOnOff,holdTraceNoneMinMax,averagingOnOff]
            if i == 4:
                trace_d_param = [updateTraceOnOff,viewTraceOnOff,holdTraceNoneMinMax,averagingOnOff]
            if i == 5:
                trace_e_param = [updateTraceOnOff,viewTraceOnOff,holdTraceNoneMinMax,averagingOnOff]
            if i == 6:
                trace_f_param = [updateTraceOnOff,viewTraceOnOff,holdTraceNoneMinMax,averagingOnOff]

        global active_trace
        active_trace = active_mkr_param[7]

        global active_trace_num
        if active_trace == 'TRA':
            active_trace_num = '1'
        elif active_trace == 'TRB':
            active_trace_num = '2'
        elif active_trace == 'TRC':
            active_trace_num = '3'
        elif active_trace == 'TRD':
            active_trace_num = '4'
        elif active_trace == 'TRE':
            active_trace_num = '5'
        elif active_trace == 'TRF':
            active_trace_num = '6'
        else:
            active_trace_num = '1'

        global active_trace_param
        if active_trace_num == '1':
            active_trace_param = trace_a_param
        elif active_trace_num == '2':
            active_trace_param = trace_b_param
        elif active_trace_num == '3':
            active_trace_param = trace_c_param
        elif active_trace_num == '4':
            active_trace_param = trace_d_param
        elif active_trace_num == '5':
            active_trace_param = trace_e_param
        elif active_trace_num == '6':
            active_trace_param = trace_f_param

    # OSNR setup is defined separately as on start-up the full amount of data needed to query the OSNR markers is not present.
    # This setup function is then called further down in the start up process to determine whether any OSNR markers are on
    def OSNRsetup(self):
        global OSNR_1_param
        global OSNR_2_param
        global OSNR_3_param
        global OSNR_4_param
        global ratio
        global active_marker
        
        ratio = math.log10(float(resBw)/float(noiseMkrBW))
        for i in range(1,5):
            if i == 1:
                itrac = "1"
                mkr_param = mkr_1_param
            if i == 2:
                itrac = "2"
                mkr_param = mkr_2_param
            if i == 3:
                itrac = "3"
                mkr_param = mkr_3_param
            if i == 4:
                itrac = "4"
                mkr_param = mkr_4_param

            if mkr_param[6] == 'ON':
                OSNRVal = float(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:RESult?" %itrac))
                OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
                OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:X:LEFT?" %itrac).rstrip()), mkr_units)
                OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:X:RIGHt?" %itrac).rstrip()), mkr_units)

                if active_trace == 'TRA':
                    trace_data = traceA
                if active_trace == 'TRB':
                    trace_data = traceB
                if active_trace == 'TRC':
                    trace_data = traceC
                if active_trace == 'TRD':
                    trace_data = traceD
                if active_trace == 'TRE':
                    trace_data = traceE
                if active_trace == 'TRF':
                    trace_data = traceF

                trace_x = trace_data[:,0]
                trace_y = trace_data[:,1]

                # have to use this method to determine the y data values as they cannot be queried directly
                error_thresh = 1
                for i in range(len(trace_x)):
                    distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
                    if distance_x < error_thresh:
                        mkr_index = i
                        error_thresh = distance_x
                OSNRyL = trace_y[mkr_index]

                error_thresh = 1
                for i in range(len(trace_x)):
                    distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
                    if distance_x < error_thresh:
                        mkr_index = i
                        error_thresh = distance_x
                OSNRyR = trace_y[mkr_index]

                OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:X:CENTer?" %itrac).rstrip()), mkr_units)

                error_thresh = 1
                for i in range(len(trace_x)):
                    distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxC)
                    if distance_x < error_thresh:
                        mkr_index = i
                        error_thresh = distance_x
                OSNRyC = trace_y[mkr_index]

                # if the OSRN value is out of range its value will be large, hence if the OSNR Y center value is greater than 100, make it 0
                OSNRyC = float(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:Y:CENTer?" %itrac))
                if OSNRyC > 100:
                    OSNRyC = 0
                    OSNRVal = 0

                if itrac == '1':
                    OSNR_1_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                    active_marker = '1'
                if itrac == '2':
                    OSNR_2_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                    active_marker = '2'
                if itrac == '3':
                    OSNR_3_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                    active_marker = '3'
                if itrac == '4':
                    OSNR_4_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                    active_marker = '4'


## ------------------------------------------------------
##      MARKER CALCULATION FUNCTIONS
## ------------------------------------------------------

    # The following functions query the machine for marker information and perform appropriate calculation to prepare them
    # for plotting and on screen text display

    def mkr1NormCalc(self):
        global mkr_1_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_1_param[0] == "1":
            markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:X?").rstrip()), mkr_units)
            markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
            mkr_1_param[1] = markerX
            mkr_1_param[2] = markerY 

    def mkr2NormCalc(self):
        global mkr_2_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_2_param[0] == "1":
            markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:X?").rstrip()), mkr_units)
            markerY = float(instrument1.query("CALCulate:MARKer2:Y?"))
            mkr_2_param[1] = markerX
            mkr_2_param[2] = markerY

    def mkr3NormCalc(self):
        global mkr_3_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_3_param[0] == "1":
            markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:X?").rstrip()), mkr_units)
            markerY = float(instrument1.query("CALCulate:MARKer3:Y?"))
            mkr_3_param[1] = markerX
            mkr_3_param[2] = markerY

    def mkr4NormCalc(self):
        global mkr_4_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_4_param[0] == "1":
            markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:X?").rstrip()), mkr_units)
            markerY = float(instrument1.query("CALCulate:MARKer4:Y?"))
            mkr_4_param[1] = markerX
            mkr_4_param[2] = markerY

    def mkr1BWCalc(self):
        global mkr_1_param
        global BW_1_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_1_param[1]
        markerY = mkr_1_param[2]
        trc = mkr_1_param[7]
        xL = str(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:LEFT?").rstrip())
        BWxL = conversions.str2float(xL, BW_units)
        xR = str(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
        BWxR = conversions.str2float(xR, BW_units)
        xC = str(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:CENTer?").rstrip())
        BWxC = conversions.str2float(xC, BW_units)
        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
        BWyL = mkr_1_param[2] + mkrBWY
        BWyR = mkr_1_param[2] + mkrBWY
        BW_1_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]

    def mkr2BWCalc(self):
        global mkr_2_param
        global BW_2_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_2_param[1]
        markerY = mkr_2_param[2]
        trc = mkr_2_param[7]
        xL = str(instrument1.query("CALCulate:MARKer2:FUNCtion:BANDwidth:X:LEFT?").rstrip())
        BWxL = conversions.str2float(xL, BW_units)
        xR = str(instrument1.query("CALCulate:MARKer2:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
        BWxR = conversions.str2float(xR, BW_units)
        xC = str(instrument1.query("CALCulate:MARKer2:FUNCtion:BANDwidth:X:CENTer?").rstrip())
        BWxC = conversions.str2float(xC, BW_units)
        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer2:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
        BWyL = mkr_2_param[2] + mkrBWY
        BWyR = mkr_2_param[2] + mkrBWY
        BW_2_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]

    def mkr3BWCalc(self):
        global mkr_3_param
        global BW_3_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_3_param[1]
        markerY = mkr_3_param[2]
        trc = mkr_3_param[7]
        xL = str(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:X:LEFT?").rstrip())
        BWxL = conversions.str2float(xL, BW_units)
        xR = str(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
        BWxR = conversions.str2float(xR, BW_units)
        xC = str(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:X:CENTer?").rstrip())
        BWxC = conversions.str2float(xC, BW_units)
        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
        BWyL = mkr_3_param[2] + mkrBWY
        BWyR = mkr_3_param[2] + mkrBWY
        BW_3_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]

    def mkr4BWCalc(self):        
        global mkr_4_param
        global BW_4_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_4_param[1]
        markerY = mkr_4_param[2]
        trc = mkr_4_param[7]
        xL = str(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:X:LEFT?").rstrip())
        BWxL = conversions.str2float(xL, BW_units)
        xR = str(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
        BWxR = conversions.str2float(xR, BW_units)
        xC = str(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:X:CENTer?").rstrip())
        BWxC = conversions.str2float(xC, BW_units)
        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
        BWyL = mkr_4_param[2] + mkrBWY
        BWyR = mkr_4_param[2] + mkrBWY
        BW_4_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]

    def mkr1DeltaCalc(self):
        global delta_distance
        global delta_1_param
        delta_distance = instrument1.query("CALC:MARK1:FUNC:DELTa:X:OFFset?")
        delta_distance = conversions.str2float(delta_distance,delta_units)
        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:X?").rstrip()),delta_units)
        markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNC:DELta:X:REF?").rstrip()),delta_units)
        markerYRef = float(instrument1.query("CALCulate:MARKer1:FUNC:DELta:Y:REF?"))
        delta_1_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]

    def mkr2DeltaCalc(self):
        global delta_distance
        global delta_2_param
        delta_distance = instrument1.query("CALC:MARK2:FUNC:DELTa:X:OFFset?")
        delta_distance = conversions.str2float(delta_distance,delta_units)
        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:X?").rstrip()),delta_units)
        markerY = float(instrument1.query("CALCulate:MARKer2:Y?"))
        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:FUNC:DELta:X:REF?").rstrip()),delta_units)
        markerYRef = float(instrument1.query("CALCulate:MARKer2:FUNC:DELta:Y:REF?"))
        delta_2_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]

    def mkr3DeltaCalc(self):
        global delta_distance
        global delta_3_param
        delta_distance = instrument1.query("CALC:MARK3:FUNC:DELTa:X:OFFset?")
        delta_distance = conversions.str2float(delta_distance,delta_units)
        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:X?").rstrip()),delta_units)
        markerY = float(instrument1.query("CALCulate:MARKer3:Y?"))
        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNC:DELta:X:REF?").rstrip()),delta_units)
        markerYRef = float(instrument1.query("CALCulate:MARKer3:FUNC:DELta:Y:REF?"))
        delta_3_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]

    def mkr4DeltaCalc(self):
        global delta_distance
        global delta_4_param
        delta_distance = instrument1.query("CALC:MARK4:FUNC:DELTa:X:OFFset?")
        delta_distance = conversions.str2float(delta_distance,delta_units)
        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:X?").rstrip()),delta_units)
        markerY = float(instrument1.query("CALCulate:MARKer4:Y?"))
        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNC:DELta:X:REF?").rstrip()),delta_units)
        markerYRef = float(instrument1.query("CALCulate:MARKer4:FUNC:DELta:Y:REF?"))
        delta_4_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]

    def mkr1OSNRCalc(self):
        global OSNR_1_param
        OSNRVal = float(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:RESult?"))
        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)

        if active_trace == 'TRA':
            trace_data = traceA
        if active_trace == 'TRB':
            trace_data = traceB
        if active_trace == 'TRC':
            trace_data = traceC
        if active_trace == 'TRD':
            trace_data = traceD
        if active_trace == 'TRE':
            trace_data = traceE
        if active_trace == 'TRF':
            trace_data = traceF

        trace_x = trace_data[:,0]
        trace_y = trace_data[:,1]
        
        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyL = trace_y[mkr_index]

        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyR = trace_y[mkr_index]

        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)

        OSNRyC = float(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:Y:CENTer?"))
        if abs(OSNRyC) > 100:
            OSNRyC = 0
            OSNRVal = 0
            self.OSNRException()

        OSNR_1_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]

    def mkr2OSNRCalc(self):
        global OSNR_2_param
        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
        OSNRVal = float(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:RESult?"))
        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
        
        if active_trace == 'TRA':
            trace_data = traceA
        if active_trace == 'TRB':
            trace_data = traceB
        if active_trace == 'TRC':
            trace_data = traceC
        if active_trace == 'TRD':
            trace_data = traceD
        if active_trace == 'TRE':
            trace_data = traceE
        if active_trace == 'TRF':
            trace_data = traceF

        trace_x = trace_data[:,0]
        trace_y = trace_data[:,1]
        
        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyL = trace_y[mkr_index]

        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyR = trace_y[mkr_index]

        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
        
        OSNRyC = float(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:Y:CENTer?"))
        if abs(OSNRyC) > 100:
            OSNRyC = 0
            OSNRVal = 0
            self.OSNRException()

        OSNR_2_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]

    def mkr3OSNRCalc(self):
        global OSNR_3_param
        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
        OSNRVal = float(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:RESult?"))
        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
        if active_trace == 'TRA':
            trace_data = traceA
        if active_trace == 'TRB':
            trace_data = traceB
        if active_trace == 'TRC':
            trace_data = traceC
        if active_trace == 'TRD':
            trace_data = traceD
        if active_trace == 'TRE':
            trace_data = traceE
        if active_trace == 'TRF':
            trace_data = traceF

        trace_x = trace_data[:,0]
        trace_y = trace_data[:,1]
        
        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyL = trace_y[mkr_index]

        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyR = trace_y[mkr_index]

        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
        
        OSNRyC = float(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:Y:CENTer?"))
        if abs(OSNRyC) > 100:
            OSNRyC = 0
            OSNRVal = 0
            self.OSNRException()

        OSNR_3_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]

    def mkr4OSNRCalc(self):
        global OSNR_4_param
        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
        OSNRVal = float(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:RESult?"))
        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
        if active_trace == 'TRA':
            trace_data = traceA
        if active_trace == 'TRB':
            trace_data = traceB
        if active_trace == 'TRC':
            trace_data = traceC
        if active_trace == 'TRD':
            trace_data = traceD
        if active_trace == 'TRE':
            trace_data = traceE
        if active_trace == 'TRF':
            trace_data = traceF

        trace_x = trace_data[:,0]
        trace_y = trace_data[:,1]
        
        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyL = trace_y[mkr_index]

        error_thresh = 1
        for i in range(len(trace_x)):
            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
            if distance_x < error_thresh:
                mkr_index = i
                error_thresh = distance_x
        OSNRyR = trace_y[mkr_index]

        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
        
        OSNRyC = float(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:Y:CENTer?"))
        if abs(OSNRyC) > 100:
            OSNRyC = 0
            OSNRVal = 0
            self.OSNRException()

        OSNR_4_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]

    def OSNRException(self):
        widget = ExceptionDialog("OSNR Not Valid. Press OK to continue.")
        widget.exec_()


## ------------------------------------------------------
##      TEXT DISPLAY FUNCTIONS
## ------------------------------------------------------

    # The marker normal displays update the displays at the top of the screen showing x and y positions and trace info.
    # The functions also update the marker parameters when called

    def mkr1NormDisplay(self):
        global mkr_1_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_1_param[0] == "1":
            markerX = mkr_1_param[1]
            markerY = mkr_1_param[2]
            amp_unit = 'dB'
            if markerY > 1e-3:
                markerY = conversions.str2float(markerY, 'mW')
                amp_unit = 'mW'
            elif markerY > 1e-6:
                markerY = conversions.str2float(markerY, 'uW')
                amp_unit = 'uW'
            elif markerY > 1e-9:
                markerY = conversions.str2float(markerY, 'nW')
                amp_unit = 'nW'
            elif markerY > 1e-12:
                markerY = conversions.str2float(markerY, 'pW')
                amp_unit = 'pW'
            trc = mkr_1_param[7]
            self.topLabel11.setText("Mkr 1 (%s)" %trc[2])
            self.topLabel12.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel13.setText("%.3f %s" %(markerY, amp_unit))
        else:
            self.topLabel11.setText("")
            self.topLabel12.setText("")
            self.topLabel13.setText("")

    def mkr2NormDisplay(self):
        global mkr_2_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_2_param[0] == "1":
            markerX = mkr_2_param[1]
            markerY = mkr_2_param[2]
            amp_unit = 'dB'
            if markerY > 1e-3:
                markerY = conversions.str2float(markerY, 'mW')
                amp_unit = 'mW'
            elif markerY > 1e-6:
                markerY = conversions.str2float(markerY, 'uW')
                amp_unit = 'uW'
            elif markerY > 1e-9:
                markerY = conversions.str2float(markerY, 'nW')
                amp_unit = 'nW'
            elif markerY > 1e-12:
                markerY = conversions.str2float(markerY, 'pW')
                amp_unit = 'pW'
            trc = mkr_2_param[7]
            self.topLabel21.setText("Mkr 2 (%s)" %trc[2])
            self.topLabel22.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel23.setText("%.3f %s" %(markerY, amp_unit))
        else:
            self.topLabel21.setText("")
            self.topLabel22.setText("")
            self.topLabel23.setText("")

    def mkr3NormDisplay(self):
        global mkr_3_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_3_param[0] == "1":
            markerX = mkr_3_param[1]
            markerY = mkr_3_param[2]
            amp_unit = 'dB'
            if markerY > 1e-3:
                markerY = conversions.str2float(markerY, 'mW')
                amp_unit = 'mW'
            elif markerY > 1e-6:
                markerY = conversions.str2float(markerY, 'uW')
                amp_unit = 'uW'
            elif markerY > 1e-9:
                markerY = conversions.str2float(markerY, 'nW')
                amp_unit = 'nW'
            elif markerY > 1e-12:
                markerY = conversions.str2float(markerY, 'pW')
                amp_unit = 'pW'
            trc = mkr_3_param[7]
            self.topLabel41.setText("Mkr 3 (%s)" %trc[2])
            self.topLabel42.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel43.setText("%.3f %s" %(markerY, amp_unit))
        else:
            self.topLabel41.setText("")
            self.topLabel42.setText("")
            self.topLabel43.setText("")

    def mkr4NormDisplay(self):
        global mkr_4_param
        # mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_4_param[0] == "1":
            markerX = mkr_4_param[1]
            markerY = mkr_4_param[2]
            amp_unit = 'dB'
            if markerY > 1e-3:
                markerY = conversions.str2float(markerY, 'mW')
                amp_unit = 'mW'
            elif markerY > 1e-6:
                markerY = conversions.str2float(markerY, 'uW')
                amp_unit = 'uW'
            elif markerY > 1e-9:
                markerY = conversions.str2float(markerY, 'nW')
                amp_unit = 'nW'
            elif markerY > 1e-12:
                markerY = conversions.str2float(markerY, 'pW')
                amp_unit = 'pW'
            trc = mkr_4_param[7]
            self.topLabel51.setText("Mkr 4 (%s)" %trc[2])
            self.topLabel52.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel53.setText("%.3f %s" %(markerY, amp_unit))
        else:
            self.topLabel51.setText("")
            self.topLabel52.setText("")
            self.topLabel53.setText("")

    # The following BWDisplays are called when the BW marker is on for the active marker. It again updates the top displays to
    # this time display bandwidth data
    def mkr1BWDisplay(self):
        global mkr_1_param
        global BW_1_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_1_param[1]
        markerY = mkr_1_param[2]
        trc = mkr_1_param[7]
        BWxL = BW_1_param[0]
        BWxR = BW_1_param[1]
        BWxC = BW_1_param[2]
        BWyL = BW_1_param[3]
        BWyR = BW_1_param[4]
        mkrBWY = BW_1_param[5]
        BWdiff = abs(BWxL-BWxR)
        self.topLabel11.setText("Mkr 1 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(markerX, mkr_units))
        self.topLabel13.setText("%.3f %s" %(markerY, amplitude_units))
        self.topLabel21.setText("Mkr 1L")
        self.topLabel22.setText("%.2f %s" %(BWxL, BW_units))
        self.topLabel23.setText("%.3f %s" %(BWyL, amplitude_units))
        self.topLabel31.setText("Mkr 1R")
        self.topLabel32.setText("%.2f %s" %(BWxR, BW_units))
        self.topLabel33.setText("%.3f %s" %(BWyR, amplitude_units))
        self.topLabel41.setText("BW")
        self.topLabel42.setText("%.2f %s" %(BWdiff, BW_units))
        self.topLabel43.setText("%.3f %s" %(mkrBWY, amplitude_units))
        self.topLabel51.setText("CWL")
        self.topLabel52.setText("%.2f %s" %(BWxC, BW_units))
        self.topLabel53.setText("")
        self.clearTopText6()

    def mkr2BWDisplay(self):
        global mkr_2_param
        global BW_2_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_2_param[1]
        markerY = mkr_2_param[2]
        trc = mkr_2_param[7]
        BWxL = BW_2_param[0]
        BWxR = BW_2_param[1]
        BWxC = BW_2_param[2]
        BWyL = BW_2_param[3]
        BWyR = BW_2_param[4]
        mkrBWY = BW_2_param[5]
        BWdiff = abs(BWxL-BWxR)
        self.topLabel11.setText("Mkr 2 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(markerX, mkr_units))
        self.topLabel13.setText("%.3f %s" %(markerY, amplitude_units))
        self.topLabel21.setText("Mkr 2L")
        self.topLabel22.setText("%.2f %s" %(BWxL, BW_units))
        self.topLabel23.setText("%.3f %s" %(BWyL, amplitude_units))
        self.topLabel31.setText("Mkr 2R")
        self.topLabel32.setText("%.2f %s" %(BWxR, BW_units))
        self.topLabel33.setText("%.3f %s" %(BWyR, amplitude_units))
        self.topLabel41.setText("BW")
        self.topLabel42.setText("%.2f %s" %(BWdiff, BW_units))
        self.topLabel43.setText("%.3f %s" %(mkrBWY, amplitude_units))
        self.topLabel51.setText("CWL")
        self.topLabel52.setText("%.2f %s" %(BWxC, BW_units))
        self.topLabel53.setText("")
        self.clearTopText6()
        BW_2_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]

    def mkr3BWDisplay(self):
        global mkr_3_param
        global BW_3_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_3_param[1]
        markerY = mkr_3_param[2]
        BWxL = BW_3_param[0]
        BWxR = BW_3_param[1]
        BWxC = BW_3_param[2]
        BWyL = BW_3_param[3]
        BWyR = BW_3_param[4]
        mkrBWY = BW_3_param[5]                                                       
        BWyL = mkr_3_param[2] + mkrBWY
        BWyR = mkr_3_param[2] + mkrBWY
        BWdiff = abs(BWxL-BWxR)
        self.topLabel11.setText("Mkr 3 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(markerX, mkr_units))
        self.topLabel13.setText("%.3f %s" %(markerY, amplitude_units))
        self.topLabel21.setText("Mkr 3L")
        self.topLabel22.setText("%.2f %s" %(BWxL, BW_units))
        self.topLabel23.setText("%.3f %s" %(BWyL, amplitude_units))
        self.topLabel31.setText("Mkr 3R")
        self.topLabel32.setText("%.2f %s" %(BWxR, BW_units))
        self.topLabel33.setText("%.3f %s" %(BWyR, amplitude_units))
        self.topLabel41.setText("BW")
        self.topLabel42.setText("%.2f %s" %(BWdiff, BW_units))
        self.topLabel43.setText("%.3f %s" %(mkrBWY, amplitude_units))
        self.topLabel51.setText("CWL")
        self.topLabel52.setText("%.2f %s" %(BWxC, BW_units))
        self.topLabel53.setText("")
        self.clearTopText6()

    def mkr4BWDisplay(self):
        global mkr_4_param
        global BW_4_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        markerX = mkr_4_param[1]
        markerY = mkr_4_param[2]
        trc = mkr_4_param[7]
        BWxL = BW_4_param[0]
        BWxR = BW_4_param[1]
        BWxC = BW_4_param[2]
        BWyL = BW_4_param[3]
        BWyR = BW_4_param[4]
        mkrBWY = BW_4_param[5]                                                       
        BWyL = mkr_4_param[2] + mkrBWY
        BWyR = mkr_4_param[2] + mkrBWY
        BWdiff = abs(BWxL-BWxR)
        self.topLabel11.setText("Mkr 4 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(markerX, mkr_units))
        self.topLabel13.setText("%.3f %s" %(markerY, amplitude_units))
        self.topLabel21.setText("Mkr 4L")
        self.topLabel22.setText("%.2f %s" %(BWxL, BW_units))
        self.topLabel23.setText("%.3f %s" %(BWyL, amplitude_units))
        self.topLabel31.setText("Mkr 4R")
        self.topLabel32.setText("%.2f %s" %(BWxR, BW_units))
        self.topLabel33.setText("%.3f %s" %(BWyR, amplitude_units))
        self.topLabel41.setText("BW")
        self.topLabel42.setText("%.2f %s" %(BWdiff, BW_units))
        self.topLabel43.setText("%.3f %s" %(mkrBWY, amplitude_units))
        self.topLabel51.setText("CWL")
        self.topLabel52.setText("%.2f %s" %(BWxC, BW_units))
        self.topLabel53.setText("")
        self.clearTopText6()

    # The noiseDisplay functions are called when the noise marker is on for the active marker
    def mkr1NoiseDisplay(self):
        global mkr_1_param
        global resBw
        global noiseMrkBW
        markerY = mkr_1_param[2]
        trc = mkr_1_param[7]
        self.topLabel11.setText("NMkr 1(%s)" %trc[2])
        self.topLabel12.setText('%.2f %s' %(mkr_1_param[1], wavelength_units))
        ratio = math.log10(float(resBw)/float(noiseMkrBW))
        ratio = markerY - 10*ratio 
        self.topLabel13.setText("%.2f %s/%snm" %(ratio, amplitude_units, noiseMkrBW))

    def mkr2NoiseDisplay(self):
        global mkr_2_param
        global resBw
        global noiseMrkBW
        markerY = mkr_2_param[2]
        trc = mkr_2_param[7]
        self.topLabel21.setText("NMkr 2(%s)" %trc[2])
        self.topLabel22.setText('%.2f %s' %(mkr_2_param[1], wavelength_units))
        ratio = math.log10(float(resBw)/float(noiseMkrBW))
        ratio = markerY - 10*ratio 
        self.topLabel23.setText("%.2f %s/%snm" %(ratio, amplitude_units, noiseMkrBW))

    def mkr3NoiseDisplay(self):
        global mkr_3_param
        global resBw
        global noiseMrkBW
        markerY = mkr_3_param[2]
        trc = mkr_3_param[7]
        self.topLabel41.setText("NMkr 3(%s)" %trc[2])
        self.topLabel42.setText('%.2f %s' %(mkr_3_param[1], wavelength_units))
        ratio = math.log10(float(resBw)/float(noiseMkrBW))
        ratio = markerY - 10*ratio 
        self.topLabel43.setText("%.2f %s/%snm" %(ratio, amplitude_units, noiseMkrBW))

    def mkr4NoiseDisplay(self):
        global mkr_4_param
        global resBw
        global noiseMrkBW
        markerY = mkr_4_param[2]
        trc = mkr_4_param[7]
        self.topLabel51.setText("NMkr 4(%s)" %trc[2])
        self.topLabel52.setText('%.2f %s' %(mkr_4_param[1], wavelength_units))
        ratio = math.log10(float(resBw)/float(noiseMkrBW))
        ratio = markerY - 10*ratio 
        self.topLabel53.setText("%.2f %s/%snm" %(ratio, amplitude_units, noiseMkrBW))

    # The DeltaDisplay functions are called when the delta marker is on for the active marker
    def mkr1DeltaDisplay(self):
        global mkr_1_param
        global delta_distance
        global delta_1_param
        trc = mkr_1_param[7]
        markerX = delta_1_param[0]
        markerY = delta_1_param[1]
        markerXRef = delta_1_param[2]
        markerYRef = delta_1_param[3]
        delta_distance = delta_1_param[4]
        self.topLabel11.setText("Delta Mkr 1")
        self.topLabel12.setText("%.3f %s" %(delta_distance,delta_units))
        deltaY = abs(markerYRef) - abs(markerY)
        self.topLabel13.setText("%.3f %s" %(deltaY,amplitude_units))
        self.topLabel21.setText("Mkr 1 Ref")
        self.topLabel22.setText("%.2f %s" %(markerXRef,delta_units))
        self.topLabel23.setText("%.3f %s" %(markerYRef,amplitude_units))
        self.topLabel31.setText("Mkr 1(%s)" %trc[2])
        self.topLabel32.setText("%.2f %s" %(markerX,delta_units))
        self.topLabel33.setText("%.3f %s" %(markerY,amplitude_units))
        self.clearTopText4()
        self.clearTopText5()
        self.clearTopText6()

    def mkr2DeltaDisplay(self):
        global mkr_2_param
        global delta_distance
        global delta_2_param
        trc = mkr_2_param[7]
        markerX = delta_2_param[0]
        markerY = delta_2_param[1]
        markerXRef = delta_2_param[2]
        markerYRef = delta_2_param[3]
        delta_distance = delta_2_param[4]
        self.topLabel11.setText("Delta Mkr 2")
        self.topLabel12.setText("%.3f %s" %(delta_distance,delta_units))
        deltaY = abs(mkr_2_param[2]) - abs(markerY)
        self.topLabel13.setText("%.3f %s" %(deltaY,amplitude_units))
        self.topLabel21.setText("Mkr 2 Ref")
        self.topLabel22.setText("%.2f %s" %(markerXRef,delta_units))
        self.topLabel23.setText("%.3f %s" %(markerYRef,amplitude_units))
        self.topLabel31.setText("Mkr 2(%s)" %trc[2])
        self.topLabel32.setText("%.2f %s" %(markerX,delta_units))
        self.topLabel33.setText("%.3f %s" %(markerY,amplitude_units))
        self.clearTopText4()
        self.clearTopText5()
        self.clearTopText6()

    def mkr3DeltaDisplay(self):
        global mkr_3_param
        global delta_distance
        global delta_3_param
        trc = mkr_3_param[7]
        markerX = delta_3_param[0]
        markerY = delta_3_param[1]
        markerXRef = delta_3_param[2]
        markerYRef = delta_3_param[3]
        delta_distance = delta_3_param[4]
        self.topLabel11.setText("Delta Mkr 3")
        self.topLabel12.setText("%.3f %s" %(delta_distance,delta_units))
        deltaY = abs(mkr_3_param[2]) - abs(markerY)
        self.topLabel13.setText("%.3f %s" %(deltaY,amplitude_units))
        self.topLabel21.setText("Mkr 3 Ref")
        self.topLabel22.setText("%.2f %s" %(markerXRef,delta_units))
        self.topLabel23.setText("%.3f %s" %(markerYRef,amplitude_units))
        self.topLabel31.setText("Mkr 3(%s)" %trc[2])
        self.topLabel32.setText("%.2f %s" %(markerX,delta_units))
        self.topLabel33.setText("%.3f %s" %(markerY,amplitude_units))
        self.clearTopText4()
        self.clearTopText5()
        self.clearTopText6()

    def mkr4DeltaDisplay(self):
        global mkr_4_param
        global delta_distance
        global delta_4_param
        markerX = delta_4_param[0]
        markerY = delta_4_param[1]
        markerXRef = delta_4_param[2]
        markerYRef = delta_4_param[3]
        delta_distance = delta_4_param[4]
        trc = mkr_4_param[7]
        self.topLabel11.setText("Delta Mkr 4")
        self.topLabel12.setText("%.3f %s" %(delta_distance,delta_units))
        deltaY = abs(mkr_4_param[2]) - abs(markerY)
        self.topLabel13.setText("%.3f %s" %(deltaY,amplitude_units))
        self.topLabel21.setText("Mkr 4 Ref")
        self.topLabel22.setText("%.2f %s" %(markerXRef,delta_units))
        self.topLabel23.setText("%.3f %s" %(markerYRef,amplitude_units))
        self.topLabel31.setText("Mkr 4(%s)" %trc[2])
        self.topLabel32.setText("%.2f %s" %(markerX,delta_units))
        self.topLabel33.setText("%.3f %s" %(markerY,amplitude_units))
        self.clearTopText4()
        self.clearTopText5()
        self.clearTopText6()

    # The OSNRDisplay functions are run when the OSNR marker is on for the active marker.
    def mkr1OSNRDisplay(self):
        global mkr_1_param
        global OSNR_1_param
        OSNRxC = OSNR_1_param[4]
        OSNRyC = OSNR_1_param[5]
        OSNRVal = OSNR_1_param[6]
        trc = mkr_2_param[7]
        self.topLabel11.setText("Mkr 1 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(mkr_1_param[1], mkr_units))
        self.topLabel13.setText("%.3f %s" %(mkr_1_param[2], amplitude_units))
        self.clearTopText2()
        self.topLabel31.setText("Center")
        self.topLabel32.setText("%.2f %s" %(OSNRxC, mkr_units))
        self.topLabel33.setText("%.3f %s" %(OSNRyC, amplitude_units))
        self.clearTopText4()
        self.topLabel51.setText("OSNR")
        self.topLabel52.setText("%0.2f %s/%snm" %(OSNRVal, amplitude_units, noiseMkrBW))
        self.topLabel53.setText("")
        self.clearTopText6()

    def mkr2OSNRDisplay(self):
        global mrk_2_param
        global OSNR_2_param
        OSNRxC = OSNR_2_param[4]
        OSNRyC = OSNR_2_param[5]
        OSNRVal = OSNR_2_param[6]
        trc = mkr_2_param[7]
        self.topLabel11.setText("Mkr 2 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(mkr_2_param[1], mkr_units))
        self.topLabel13.setText("%.3f %s" %(mkr_2_param[2], amplitude_units))
        self.clearTopText2()
        self.topLabel31.setText("Center")
        self.topLabel32.setText("%.2f %s" %(OSNRxC, mkr_units))
        self.topLabel33.setText("%.3f %s" %(OSNRyC, amplitude_units))
        self.clearTopText4()
        self.topLabel51.setText("OSNR")
        self.topLabel52.setText("%0.2f %s/%snm" %(OSNRVal, amplitude_units, noiseMkrBW))
        self.topLabel53.setText("")
        self.clearTopText6()

    def mkr3OSNRDisplay(self):
        global mkr_3_param
        global OSNR_3_param
        OSNRxC = OSNR_3_param[4]
        OSNRyC = OSNR_3_param[5]
        OSNRVal = OSNR_3_param[6]
        trc = mkr_3_param[7]
        self.topLabel11.setText("Mkr 3 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(mkr_3_param[1], mkr_units))
        self.topLabel13.setText("%.3f %s" %(mkr_3_param[2], amplitude_units))
        self.clearTopText2()
        self.topLabel31.setText("Center")
        self.topLabel32.setText("%.2f %s" %(OSNRxC, mkr_units))
        self.topLabel33.setText("%.3f %s" %(OSNRyC, amplitude_units))
        self.clearTopText4()
        self.topLabel51.setText("OSNR")
        self.topLabel52.setText("%0.2f %s/%snm" %(OSNRVal, amplitude_units, noiseMkrBW))
        self.topLabel53.setText("")
        self.clearTopText6()

    def mkr4OSNRDisplay(self):
        global mkr_4_param
        global OSNR_4_param
        OSNRxC = OSNR_4_param[4]
        OSNRyC = OSNR_4_param[5]
        OSNRVal = OSNR_4_param[6]
        trc = mkr_4_param[7]
        self.topLabel11.setText("Mkr 4 (%s)" %trc[2])
        self.topLabel12.setText("%.2f %s" %(mkr_4_param[1], mkr_units))
        self.topLabel13.setText("%.3f %s" %(mkr_4_param[2], amplitude_units))
        self.clearTopText2()
        self.topLabel31.setText("Center")
        self.topLabel32.setText("%.2f %s" %(OSNRxC, mkr_units))
        self.topLabel33.setText("%.3f %s" %(OSNRyC, amplitude_units))
        self.clearTopText4()
        self.topLabel51.setText("OSNR")
        self.topLabel52.setText("%0.2f %s/%snm" %(OSNRVal, amplitude_units, noiseMkrBW))
        self.topLabel53.setText("")
        self.clearTopText6()

    # Marker comparison display creates the display showing the comparison between markers 1 and 2 and/or markers 3 and 4.
    def mkrCompDisplay(self):
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param
        if mkr_1_param[0] == "1":
            if mkr_2_param[0] == "1":
                self.topLabel31.setText("Mkr 2-1")
                markerDiffWL = mkr_2_param[1]-mkr_1_param[1]
                if mkr_1_param[4] == 'ON':
                    ratio = math.log10(float(resBw)/float(noiseMkrBW))
                    mkr1y = mkr_1_param[2] - 10*ratio 
                else:
                    mkr1y = mkr_1_param[2]
                if mkr_2_param[4] == 'ON':
                    ratio = math.log10(float(resBw)/float(noiseMkrBW))
                    mkr2y = mkr_2_param[2] - 10*ratio 
                else:
                    mkr2y = mkr_2_param[2]
                if amplitude_units == 'W':
                    markerDiffAmp = mkr_2_param[2]/mkr_1_param[2]
                    self.topLabel33.setText("%.3f" %markerDiffAmp)
                else:
                    markerDiffAmp = mkr2y - mkr1y
                    self.topLabel33.setText("%.3f %s" %(markerDiffAmp,amplitude_units))
                self.topLabel32.setText("%.2f %s" %(markerDiffWL,wavelength_units))
                
            else:
                self.topLabel31.setText("")
                self.topLabel32.setText("")
                self.topLabel33.setText("")
        else:
            self.topLabel31.setText("")
            self.topLabel32.setText("")
            self.topLabel33.setText("")

        if mkr_3_param[0] == "1":
            if mkr_4_param[0] == "1":
                self.topLabel61.setText("Mkr 4-3")
                markerDiffWL = mkr_4_param[1]-mkr_3_param[1]
                if mkr_3_param[4] == 'ON':
                    ratio = math.log10(float(resBw)/float(noiseMkrBW))
                    mkr3y = mkr_3_param[2] - 10*ratio 
                else:
                    mkr3y = mkr_3_param[2]
                if mkr_4_param[4] == 'ON':
                    ratio = math.log10(float(resBw)/float(noiseMkrBW))
                    mkr4y = mkr_4_param[2] - 10*ratio 
                else:
                    mkr4y = mkr_4_param[2]
                if amplitude_units == 'W':
                    markerDiffAmp = mkr_4_param[2]/mkr_3_param[2]
                    self.topLabel63.setText("%.3f" %markerDiffAmp)
                else:
                    markerDiffAmp = mkr4y - mkr3y
                    self.topLabel63.setText("%.3f %s" %(markerDiffAmp,amplitude_units))
                self.topLabel62.setText("%.2f %s" %(markerDiffWL,wavelength_units))
                
            else:
                self.topLabel61.setText("")
                self.topLabel62.setText("")
                self.topLabel63.setText("")
        else:
            self.topLabel61.setText("")
            self.topLabel62.setText("")
            self.topLabel63.setText("")

    def mkr1ContDisplay(self):
        if mkr_1_param[3] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr1BWCalc()
            self.mkr1BWDisplay()
        elif mkr_1_param[4] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
            self.mkr1NoiseDisplay()
            if repeatSweepOnOff == 'OFF':
                self.mkr2NormCalc()
                self.mkr3NormCalc()
                self.mkr4NormCalc()
            if mkr_2_param[4] == 'ON':
                self.mkr2NoiseDisplay()
            else:
                self.mkr2NormDisplay()
            if mkr_3_param[4] == 'ON':
                self.mkr3NoiseDisplay()
            else:
                self.mkr3NormDisplay()
            if mkr_4_param[4] == 'ON':
                self.mkr4NoiseDisplay()
            else:
                self.mkr4NormDisplay()
            self.mkrCompDisplay()
        elif mkr_1_param[5] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr1DeltaCalc()
            self.mkr1DeltaDisplay()
        elif mkr_1_param[6] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr1OSNRCalc()
            self.mkr1OSNRDisplay()
        else:
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr2NormCalc()
                self.mkr3NormCalc()
                self.mkr4NormCalc()
            self.mkr1NormDisplay()
            self.mkr2NormDisplay()
            self.mkr3NormDisplay()
            self.mkr4NormDisplay()
            self.mkrCompDisplay()

    def mkr2ContDisplay(self):
        if mkr_2_param[3] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr2NormCalc()
                self.mkr2BWCalc()
            self.mkr2BWDisplay()
        elif mkr_2_param[4] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr2NormCalc()
            self.mkr2NoiseDisplay()
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr3NormCalc()
                self.mkr4NormCalc()
            if mkr_1_param[4] == 'ON':
                self.mkr1NoiseDisplay()
            else:
                self.mkr1NormDisplay()
            if mkr_3_param[4] == 'ON':
                self.mkr3NoiseDisplay()
            else:
                self.mkr3NormDisplay()
            if mkr_4_param[4] == 'ON':
                self.mkr4NoiseDisplay()
            else:
                self.mkr4NormDisplay()
            self.mkrCompDisplay()
        elif mkr_2_param[5] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr2DeltaCalc()
            self.mkr2DeltaDisplay()
        elif mkr_2_param[6] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr2NormCalc()
                self.mkr2OSNRCalc()
            self.mkr2OSNRDisplay()
        else:
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr2NormCalc()
                self.mkr3NormCalc()
                self.mkr4NormCalc()
            self.mkr1NormDisplay()
            self.mkr2NormDisplay()
            self.mkr3NormDisplay()
            self.mkr4NormDisplay()
            self.mkrCompDisplay()

    def mkr3ContDisplay(self):
        if mkr_3_param[3] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr3NormCalc()
                self.mkr3BWCalc()
            self.mkr3BWDisplay()
        elif mkr_3_param[4] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr3NormCalc()
            self.mkr3NoiseDisplay()
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr2NormCalc()
                self.mkr4NormCalc()
            if mkr_1_param[4] == 'ON':
                self.mkr1NoiseDisplay()
            else:
                self.mkr1NormDisplay()
            if mkr_2_param[4] == 'ON':
                self.mkr2NoiseDisplay()
            else:
                self.mkr3NormDisplay()
            if mkr_4_param[4] == 'ON':
                self.mkr4NoiseDisplay()
            else:
                self.mkr4NormDisplay()
            self.mkrCompDisplay()
        elif mkr_3_param[5] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr3DeltaCalc()
            self.mkr3DeltaDisplay()
        elif mkr_3_param[6] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr3NormCalc()
                self.mkr3OSNRCalc()
            self.mkr3OSNRDisplay()
        else:
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr2NormCalc()
                self.mkr3NormCalc()
                self.mkr4NormCalc()
            self.mkr1NormDisplay()
            self.mkr2NormDisplay()
            self.mkr3NormDisplay()
            self.mkr4NormDisplay()
            self.mkrCompDisplay()

    def mkr4ContDisplay(self):
        if mkr_4_param[3] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr4NormCalc()
                self.mkr4BWCalc()
            self.mkr4BWDisplay()
        elif mkr_4_param[4] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr4NormCalc()
            self.mkr4NoiseDisplay()
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr2NormCalc()
                self.mkr3NormCalc()
            if mkr_1_param[4] == 'ON':
                self.mkr1NoiseDisplay()
            else:
                self.mkr1NormDisplay()
            if mkr_2_param[4] == 'ON':
                self.mkr2NoiseDisplay()
            else:
                self.mkr2NormDisplay()
            if mkr_3_param[4] == 'ON':
                self.mkr3NoiseDisplay()
            else:
                self.mkr3NormDisplay()
            self.mkrCompDisplay()
        elif mkr_4_param[5] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr4DeltaCalc()
            self.mkr4DeltaDisplay()
        elif mkr_4_param[6] == "ON":
            if repeatSweepOnOff == 'OFF':
                self.mkr4NormCalc()
                self.mkr4OSNRCalc()
            self.mkr4OSNRDisplay()
        else:
            if repeatSweepOnOff == 'OFF':
                self.mkr1NormCalc()
                self.mkr2NormCalc()
                self.mkr3NormCalc()
                self.mkr4NormCalc()
            self.mkr1NormDisplay()
            self.mkr2NormDisplay()
            self.mkr3NormDisplay()
            self.mkr4NormDisplay()
            self.mkrCompDisplay()

    def setActMkr(self):
        global active_marker

        if active_marker == '1':
            instrument1.write("CALCulate:MARKer1:STATe ON")
        elif active_marker == '2':
            instrument1.write("CALCulate:MARKer1:STATe ON")
        elif active_marker == '3':
            instrument1.write("CALCulate:MARKer1:STATe ON")
        elif active_marker == '4':
            instrument1.write("CALCulate:MARKer1:STATe ON")

    # Info display creates the display of information based at the bottom of the display.
    def infoDisplay(self):
        global resBw
        global vidBw
        global sensitivity
        global sweepTime
        global integValue
        global active_trace_param
        
        value = instrument1.query("SENSe:BANDwidth:RESolution?")
        resBw = conversions.str2float(value,"%s" %wavelength_units)
        self.btmLabel21.setText("%.2f %s" %(resBw, wavelength_units))

        value = instrument1.query("SENSe:BANDwidth:VIDeo?")
        vidBw = conversions.str2float(value,"%s" %frequency_units)
        self.btmLabel22.setText("%.2f %s" %(vidBw, frequency_units))

        value = str(instrument1.query("SENSe:POWer:DC:RANGe:LOWer?"))
        sensitivity = float(value)
        self.btmLabel41.setText("%.2f dBm" %sensitivity)

        value = instrument1.query("SENSe:SWEep:TIME?")
        sweepTime = float(value)
        self.btmLabel42.setText("%.3f s" %sweepTime)

        if str(instrument1.query("CALCulate:TPOWer:STATe?").rstrip()) == '1':
            integValue = instrument1.query("CALCulate:TPOWer:DATA?")
            integValue = float(integValue)
            self.btmLabel61.setText("%0.2f dBm" %integValue)
        else:
            self.btmLabel61.setText("")

        self.btmLabel62.setText("%s" %active_trace_param[3])
        self.btmLabel71.setText("In %s" %wavelengthRefIn)


## ------------------------------------------------------
##          MENUS
## ------------------------------------------------------
   
    # Function to clear current sub-menu when new menu is needed
    def clearLayout(self, layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clearLayout(child.layout())

    # If the machine is still updating the display or reading functions, prevent the user from performing a new function
    def updatingException(self):
        widget = ExceptionDialog("Machine still updating. Press OK to continue.")
        widget.exec_()
        self.goToMenu()
    
    # Some functions are not available while repeat sweep is on. Prevent the user from accessing these 
    def sweepException(self):
        widget = ExceptionDialog("Function not available while repeat sweep is on.")
        widget.exec_()

    def plotException(self):
        widget = ExceptionDialog("Plot cannot be added, data out of range.")
        widget.exec_()

    def sweepThreadOn(self):
        self.contSweep = Thread()
        self.contSweep.sig.connect(self.contPlot)
        self.contSweep.sig2.connect(self.contPlotStop)
        self.contSweep.sig3.connect(self.goToMenu)
        self.contSweep.start()
        
    def goToMenu(self):
        if menuFlag == 'top':
            self.topMenu()
        elif menuFlag == 'wavelength':
            self.wavelengthMenu()
        elif menuFlag == 'amplitude':
            self.amplitudeMenu()
        elif menuFlag == 'markers':
            self.markersMenu()
        elif menuFlag == 'moreMarkers':
            self.moreMkrFunc()
        elif menuFlag == 'searchMarkers':
            self.mkrSrchMenu()
        elif menuFlag == 'lineMarkers':
            self.lineMkrMenu()
        elif menuFlag == 'traces':
            self.tracesMenu()
        elif menuFlag == 'traceMath':
            self.trceMath()
        elif menuFlag == 'bandwidth':
            self.bwMenu()
        elif menuFlag == 'moreBandwidth':
            self.moreBWFunc()

    # Wavelength sub-menu
    # The wavelength menu buttons are defined here. On click the buttons will load the associated function from below.
    
    # All of the menus work in the same basic manor: when the button is clicked the menu action is loaded. The current value
    # is queried from the machine and converted into the correct format for display/manipulation. This value is added into the
    # dialog box for the user to see. If the user changes the value in the box and hits ok, the function writes the user input
    # value to the machine. The trace and marker display functions are called to update the marker and trace on the display.
    # If no action is required from the user, the button simply triggers a write to the machine and runs the display functions.
    def wavelengthMenu(self):
        global menuFlag
        menuFlag = 'wavelength'

        self.clearLayout(self.subButtonLayout)
        self.buttonCenterWL = QtWidgets.QPushButton("Center WL", self)
        self.buttonCenterWL.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonCenterWL)
        self.buttonSpan = QtWidgets.QPushButton("Span", self)
        self.buttonSpan.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonSpan)
        self.buttonStartWL = QtWidgets.QPushButton("Start WL", self)
        self.buttonStartWL.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonStartWL)
        self.buttonStopWL = QtWidgets.QPushButton("Stop WL", self)
        self.buttonStopWL.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonStopWL)
        self.buttonPeakToCenter = QtWidgets.QPushButton("Peak To Center", self)
        self.buttonPeakToCenter.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPeakToCenter)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonWavelengthSetup = QtWidgets.QPushButton("Wavelength Setup", self)
        self.buttonWavelengthSetup.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonWavelengthSetup)

        if reset == 0:
            self.buttonCenterWL.clicked.connect(self.centerWL)
            self.buttonSpan.clicked.connect(self.span)
            self.buttonStartWL.clicked.connect(self.startWL)
            self.buttonStopWL.clicked.connect(self.stopWL)
            self.buttonPeakToCenter.clicked.connect(self.peakToCenter)
            self.buttonWavelengthSetup.clicked.connect(self.wavelengthSetupWindow)
        else:
            self.buttonCenterWL.clicked.connect(self.updatingException)
            self.buttonSpan.clicked.connect(self.updatingException)
            self.buttonStartWL.clicked.connect(self.updatingException)
            self.buttonStopWL.clicked.connect(self.updatingException)
            self.buttonPeakToCenter.clicked.connect(self.updatingException)
            self.buttonWavelengthSetup.clicked.connect(self.updatingException)

    def centerWL(self):
        global inUse
        global plotDone
        global contOnOff
        global reset
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("SENSe:WAVelength:CENTer?")
        current_value = str(conversions.str2float(value,"%s"%wavelength_units))
        widget = InputDialog("Center WL", "%s" %wavelength_units, current_value)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            wavelength = "SENSe:WAVelength:CENTer " + "%s%s" %(widget.userInput,wavelength_units)
            instrument1.write(wavelength)
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def span(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("SENSe:WAVelength:SPAN?")
        current_value = str(conversions.str2float(value,"%s"%wavelength_units))
        widget = InputDialog("Span", "%s" %wavelength_units, current_value)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            wavelength = "SENSe:WAVelength:SPAN " + "%s%s" %(widget.userInput,wavelength_units)
            instrument1.write(wavelength)
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def startWL(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("SENSe:WAVelength:STARt?")
        current_value = str(conversions.str2float(value,"%s" %wavelength_units))
        widget = InputDialog("Start WL", "%s" %wavelength_units, current_value)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            wavelength = "SENSe:WAVelength:STARt " + "%s%s" %(widget.userInput,wavelength_units)
            instrument1.write(wavelength)
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0

    def stopWL(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("SENSe:WAVelength:STOP?")
        current_value = str(conversions.str2float(value,"%s" %wavelength_units))
        widget = InputDialog("Stop WL", "%s" %wavelength_units, current_value)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            wavelength = "SENSe:WAVelength:STOP " + "%s%s" %(widget.userInput,wavelength_units)
            instrument1.write(wavelength)
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def peakToCenter(self):
        global inUse
        global plotDone
        global reset
        global contOnOff

        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate:MARK:SCENter")
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Brings up the wavelength setup window
    def wavelengthSetupWindow(self): 
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        widget = WavelengthSetup(parent=self)
        widget.exec_()
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        

    # Amplitude sub-menu

    # All of the menus work in the same basic manor: when the button is clicked the menu action is loaded. The current value
    # is queried from the machine and converted into the correct format for display/manipulation. This value is added into the
    # dialog box for the user to see. If the user changes the value in the box and hits ok, the function writes the user input
    # value to the machine. The trace and marker display functions are called to update the marker and trace on the display.
    # If no action is required from the user, the button simply triggers a write to the machine and runs the display functions.
    # If the button is a toggle button, then it works the same as the trigger, but also changes the text of the displayed button.
    def amplitudeMenu(self):
        global logLin    
        global autoMan
        global traceIntOnOff
        global amplitude_units
        global menuFlag
        menuFlag = 'amplitude'

        self.clearLayout(self.subButtonLayout)
        self.buttonRefLvl = QtWidgets.QPushButton("Reference Level", self)
        self.buttonRefLvl.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonRefLvl)
        self.buttonScaleDiv = QtWidgets.QPushButton("Scale/Div", self)
        self.buttonScaleDiv.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonScaleDiv)
        self.buttonDispMode = QtWidgets.QPushButton("Display Mode [%s]" %logLin, self)
        self.buttonSensitivity = QtWidgets.QPushButton("Sensitivity [%s]" %autoMan, self)
        self.buttonTraceInteg = QtWidgets.QPushButton("Trace Integ [%s]" %traceIntOnOff, self)
        if reset == 0:
            self.menuDispMode = QtWidgets.QMenu()
            self.menuDispMode.addAction("LOG", self.DispModeAction1)
            self.menuDispMode.addAction("LIN", self.DispModeAction2)
            self.buttonDispMode.setMenu(self.menuDispMode)
            self.menuSensitivity = QtWidgets.QMenu()
            self.menuSensitivity.addAction("AUTO", self.SensitivityAction1)
            self.menuSensitivity.addAction("MAN", self.SensitivityAction2)
            self.buttonSensitivity.setMenu(self.menuSensitivity)
            self.menuTraceInteg = QtWidgets.QMenu()
            self.menuTraceInteg.addAction("On", self.TraceIntegAction1)
            self.menuTraceInteg.addAction("Off", self.TraceIntegAction2)
            self.buttonTraceInteg.setMenu(self.menuTraceInteg)
        else:
            self.buttonDispMode.clicked.connect(self.updatingException)
            self.buttonSensitivity.clicked.connect(self.updatingException)
            self.buttonTraceInteg.clicked.connect(self.updatingException)
        self.buttonDispMode.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonDispMode)
        self.buttonSensitivity.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonSensitivity)
        self.buttonPeakToRefLvl = QtWidgets.QPushButton("Peak To Ref Level", self)
        self.buttonPeakToRefLvl.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPeakToRefLvl)
        self.buttonTraceInteg.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonTraceInteg)
        self.buttonAmplitudeSetup = QtWidgets.QPushButton("Amplitude Setup", self)
        self.buttonAmplitudeSetup.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonAmplitudeSetup)

        if reset == 0:
            self.buttonRefLvl.clicked.connect(self.refLVL)
            self.buttonScaleDiv.clicked.connect(self.scaleDiv)
            self.buttonPeakToRefLvl.clicked.connect(self.peakToRefLvl)
            self.buttonAmplitudeSetup.clicked.connect(self.amplitudeSetupWindow)
        else:
            self.buttonRefLvl.clicked.connect(self.updatingException)
            self.buttonScaleDiv.clicked.connect(self.updatingException)
            self.buttonPeakToRefLvl.clicked.connect(self.updatingException)
            self.buttonAmplitudeSetup.clicked.connect(self.updatingException)  

    def refLVL(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("DISPlay:WINDow:TRACe:Y:SCALe:RLEVel?")
        current_value = str(conversions.str2float(value,"%s" %amplitude_units))
        widget = InputDialog("Reference Level", "%s" %amplitude_units, current_value)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            level = "DISPlay:WINDow:TRACe:Y:SCALe:RLEVel " + "%sdBm" %widget.userInput
            instrument1.write(level)
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def scaleDiv(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("DISPlay:WINDow:TRACe:Y:SCALe:PDIVision?")
        current_value = str(conversions.str2float(value,"%s" %amplitude_units))
        widget = InputDialog("Scale/Div", "%s" %amplitude_units, current_value)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            scale = "DISPlay:WINDow:TRACe:Y:SCALe:PDIVision " + "%s%s" %(widget.userInput,amplitude_units)
            instrument1.write(scale)
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def DispModeAction1(self):
        global amplitude_units
        global logLin
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonDispMode.setText("Display Mode [LOG]")
        instrument1.write("DISPlay:WINDow:TRACe:Y:SCALe:SPACing LOG")
        amplitude_units = 'dB'
        logLin = 'LOG'
        sweep = 1
        if repeatSweepOnOff == "OFF":
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def DispModeAction2(self): 
        global amplitude_units
        global logLin
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonDispMode.setText("Display Mode [LIN]")
        instrument1.write("DISPlay:WINDow:TRACe:Y:SCALe:SPACing LIN")
        amplitude_units = 'W'
        logLin = 'LIN'
        sweep = 1
        if repeatSweepOnOff == "OFF":
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def SensitivityAction1(self):
        global sensitivity
        global inUse
        global plotDone
        global reset
        global contOnOff
        global autoMan
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonSensitivity.setText("Sensitivity [AUTO]")
        instrument1.write("SENSe:POWer:DC:RANGe:LOWer:AUTO ON")
        autoMan = 'AUTO'
        sensitivity = str(instrument1.query("SENSe:POWer:DC:RANGe:LOWer?"))
        sensitivity = str(conversions.str2float(sensitivity, amplitude_units))
        sweep = 0
        if repeatSweepOnOff == "OFF":
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
                
    def SensitivityAction2(self): 
        global sensitivity
        global inUse
        global plotDone
        global reset
        global contOnOff
        global autoMan
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        sensitivity = str(instrument1.query("SENSe:POWer:DC:RANGe:LOWer?"))
        sensitivity = str(conversions.str2float(sensitivity, amplitude_units))
        widget = InputDialog("Sensitivity", "%s" %amplitude_units, sensitivity)
        widget.exec_()
        sweep = 0
        if widget.userInput != 0:
            sensitivity = widget.userInput
            instrument1.write("SENSe:POWer:DC:RANGe:LOWer:AUTO OFF")
            sensitivityStr = "SENSe:POWer:DC:RANGe:LOWer " + "%sdBm" %widget.userInput
            instrument1.write(sensitivityStr)
            self.buttonSensitivity.setText("Sensitivity [MAN]")
            autoMan = 'MAN'
            if repeatSweepOnOff == "OFF":
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def peakToRefLvl(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate:MARKer:SRLevel")
        sweep = 0
        if repeatSweepOnOff == "OFF":
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TraceIntegAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global traceIntOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTraceInteg.setText("Trace Integ [ON]")
        instrument1.write("CALCulate%s:TPOWer:STATe ON" %active_trace_num)
        traceIntOnOff = 'ON'
        sweep = 0
        if repeatSweepOnOff == "OFF":
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
            self.infoDisplay()
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TraceIntegAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global traceIntOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTraceInteg.setText("Trace Integ [OFF]")
        instrument1.write("CALCulate%s:TPOWer:STATe OFF" %active_trace_num)
        traceIntOnOff = 'OFF'
        sweep = 0
        if repeatSweepOnOff == "OFF":
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Brings up the amplitude setup menu
    def amplitudeSetupWindow(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        widget = AmplitudeSetup()
        widget.exec_()
        if repeatSweepOnOff == "ON":
            reset = 1
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        

    # Markers sub-menu

    # There are several sub-menu layers to this as markers are a large part of the machine function
    def markersMenu(self):
        global menuFlag
        menuFlag = 'markers'

        self.clearLayout(self.subButtonLayout) 
        self.buttonActMrks = QtWidgets.QPushButton("Displayed Markers", self)
        self.buttonActMrks.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonActMrks)
        self.buttonPeakSrch = QtWidgets.QPushButton("Peak Search", self)
        self.buttonPeakSrch.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPeakSrch)
        self.buttonMkrToCen = QtWidgets.QPushButton("Marker %s to Center" %active_marker, self)
        self.buttonMkrToCen.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMkrToCen)
        self.buttonMkrToRefLvl = QtWidgets.QPushButton("Marker %s To Ref Level" %active_marker, self)
        self.buttonMkrToRefLvl.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMkrToRefLvl)
        self.buttonMkrSetup = QtWidgets.QPushButton("Marker Setup", self)
        self.buttonMkrSetup.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMkrSetup)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonMoreMkrFunc = QtWidgets.QPushButton("More Marker Functons", self)
        self.buttonMoreMkrFunc.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMoreMkrFunc)

        if reset == 0:
            self.buttonActMrks.clicked.connect(self.actMrks)
            self.buttonPeakSrch.clicked.connect(self.peakSearch)
            self.buttonMkrToCen.clicked.connect(self.mrkToCen)
            self.buttonMkrToRefLvl.clicked.connect(self.mkrToRefLvl)
            self.buttonMkrSetup.clicked.connect(self.mkrSetup)        
        else:
            self.buttonActMrks.clicked.connect(self.updatingException)
            self.buttonPeakSrch.clicked.connect(self.updatingException)
            self.buttonMkrToCen.clicked.connect(self.updatingException)
            self.buttonMkrToRefLvl.clicked.connect(self.updatingException)
            self.buttonMkrSetup.clicked.connect(self.updatingException)
        self.buttonMoreMkrFunc.clicked.connect(self.moreMkrFunc)

    # Brings up the active markers window to select which markers should be displayed
    def actMrks(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        widget = ActiveMarkersWindow()
        widget.exec_()
        if widget.markerReturn == 1:
            self.mkr1NormCalc()
            self.mkr1NormDisplay()
            self.mkr2NormCalc()
            self.mkr2NormDisplay()
            self.mkr3NormCalc()
            self.mkr3NormDisplay()
            self.mkr4NormCalc()
            self.mkr4NormDisplay()
            self.mkrCompDisplay()
            self.markerPlot()
            self.buttonActMkrGbl.setText("Mkr %s" %active_marker)
            self.markerPlot()
        if repeatSweepOnOff == "ON":
            reset = 1
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def peakSearch(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate:MARKer%s:MAXimum" %active_marker)
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def mrkToCen(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate:MARKer%s:SCENter" %active_marker)
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def mkrToRefLvl(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate:MARKer%s:SRLevel" %active_marker)
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Brings up the marker setup menu for the active marker
    def mkrSetup(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        widget = MarkerSetup("%s" %active_marker)
        widget.exec_()
        self.threshPlot()
        if repeatSweepOnOff == "OFF":
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    # Further sub-menu for more marker functions
    def moreMkrFunc(self):
        global menuFlag
        menuFlag = 'moreMarkers' # Allows redraw back to this menu if a different marker is made active

        self.clearLayout(self.subButtonLayout) 
        self.buttonMkrSrchMenu = QtWidgets.QPushButton("Marker Search Menu", self)
        self.buttonMkrSrchMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMkrSrchMenu)
        self.buttonMkrBW = QtWidgets.QPushButton("Marker %s Bandwidth [%s]" %(active_marker, active_mkr_param[3]), self)
        self.buttonMkrBW.setCheckable(1)
        self.buttonMkrBW.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMkrBW)
        self.buttonNoiseMkr = QtWidgets.QPushButton("Noise Marker %s [%s]" %(active_marker, active_mkr_param[4]), self)
        self.buttonNoiseMkr.setCheckable(1)
        self.buttonNoiseMkr.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonNoiseMkr)
        self.buttonDeltaMkr = QtWidgets.QPushButton("Delta Marker %s [%s]" %(active_marker, active_mkr_param[5]), self)
        self.buttonDeltaMkr.setCheckable(1)
        self.buttonDeltaMkr.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonDeltaMkr)
        self.buttonOSNRMkr = QtWidgets.QPushButton("OSNR Marker %s [%s]" %(active_marker, active_mkr_param[6]), self)
        self.buttonOSNRMkr.setCheckable(1)
        self.buttonOSNRMkr.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonOSNRMkr)
        self.buttonLineMkrMenu = QtWidgets.QPushButton("Line Marker Menu", self)
        self.buttonLineMkrMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonLineMkrMenu)
        self.buttonPrevMenu = QtWidgets.QPushButton("Previous Menu", self)
        self.buttonPrevMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPrevMenu)

        if reset == 0:  
            self.buttonMkrBW.clicked.connect(self.mkrBWOnOff)
            self.buttonNoiseMkr.clicked.connect(self.noiseMkr)
            self.buttonDeltaMkr.clicked.connect(self.deltaMkr)
            self.buttonOSNRMkr.clicked.connect(self.OSNRMkr)             
        else:
            self.buttonMkrBW.clicked.connect(self.updatingException)
            self.buttonNoiseMkr.clicked.connect(self.updatingException)
            self.buttonDeltaMkr.clicked.connect(self.updatingException)
            self.buttonOSNRMkr.clicked.connect(self.updatingException)
        self.buttonMkrSrchMenu.clicked.connect(self.mkrSrchMenu)
        self.buttonLineMkrMenu.clicked.connect(self.lineMkrMenu) 
        self.buttonPrevMenu.clicked.connect(self.markersMenu)

    # Further sub-menu for marker search functions
    def mkrSrchMenu(self):
        self.clearLayout(self.subButtonLayout) 
        global menuFlag
        menuFlag = 'searchMarkers'
        
        self.buttonSrchMode = QtWidgets.QPushButton("Search Mode [%s]" %peakPit, self)
        self.buttonSrchMode.setCheckable(1)
        self.buttonSrchMode.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonSrchMode)
        self.buttonPeakSrch = QtWidgets.QPushButton("%s Search" %peakPit, self)
        self.buttonPeakSrch.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPeakSrch)
        self.buttonNextPeakDown = QtWidgets.QPushButton("Next %s %s" %(peakPit,upDown), self)
        self.buttonNextPeakDown.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonNextPeakDown)
        self.buttonNextPeakLeft = QtWidgets.QPushButton("Next %s Left" %peakPit, self)
        self.buttonNextPeakLeft.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonNextPeakLeft)
        self.buttonNextPeakRight = QtWidgets.QPushButton("Next %s Right" %peakPit, self)
        self.buttonNextPeakRight.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonNextPeakRight)
        self.buttonActMrks = QtWidgets.QPushButton("", self)
        self.buttonActMrks.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonActMrks)
        self.buttonPrevMenu = QtWidgets.QPushButton("Previous Menu", self)
        self.buttonPrevMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPrevMenu)

        if reset == 0:
            self.buttonSrchMode.clicked.connect(self.srchMode)
            self.buttonPeakSrch.clicked.connect(self.peakSrch)
            self.buttonNextPeakDown.clicked.connect(self.nextDown)
            self.buttonNextPeakLeft.clicked.connect(self.nextLeft)
            self.buttonNextPeakRight.clicked.connect(self.nextRight)
        else:
            self.buttonSrchMode.clicked.connect(self.updatingException)
            self.buttonPeakSrch.clicked.connect(self.updatingException)
            self.buttonNextPeakDown.clicked.connect(self.updatingException)
            self.buttonNextPeakLeft.clicked.connect(self.updatingException)
            self.buttonNextPeakRight.clicked.connect(self.updatingException)
        self.buttonPrevMenu.clicked.connect(self.moreMkrFunc)

    def srchMode(self):
        global peakPit
        global upDown
        if peakPit == "PEAK":
            upDown = "Up"
            self.buttonSrchMode.setText("Search Mode [PIT]")
            self.buttonPeakSrch.setText("Pit Search")
            self.buttonNextPeakDown.setText("Next Pit Up")
            self.buttonNextPeakLeft.setText("Next Pit Left")
            self.buttonNextPeakRight.setText("Next Pit Right")
            peakPit = "PIT"
        elif peakPit == "PIT":
            upDown = "Down"
            self.buttonSrchMode.setText("Search Mode [PEAK]")
            self.buttonPeakSrch.setText("Peak Search")
            self.buttonNextPeakDown.setText("Next Peak Down")
            self.buttonNextPeakLeft.setText("Next Peak Left")
            self.buttonNextPeakRight.setText("Next Peak Right")
            peakPit = "PEAK"

    def peakSrch(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        if peakPit == "PEAK":
            instrument1.write("CALCulate:MARKer%s:MAX" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif peakPit == "PIT":
            instrument1.write("CALCulate:MARKer%s:MIN" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def nextDown(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        if peakPit == "PEAK":
            instrument1.write("CALCulate:MARKer%s:MAX:NEXT" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif peakPit == "PIT":
            instrument1.write("CALCulate:MARKer%s:MIN:NEXT" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def nextLeft(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        if peakPit == "PEAK":
            instrument1.write("CALCulate:MARKer%s:MAX:LEFT" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif peakPit == "PIT":
            instrument1.write("CALCulate:MARKer%s:MIN:LEFT" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def nextRight(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        if peakPit == "PEAK":
            instrument1.write("CALCulate:MARKer%s:MAX:RIGH" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif peakPit == "PIT":
            instrument1.write("CALCulate:MARKer%s:MIN:RIGH" %active_marker)
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def mkrBWOnOff(self): 
        global markerBWOnOff
        global active_mkr_param
        global mrkBWY
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        markerBWOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe?" %active_marker)).rstrip()
        restartThread = 0
        if markerBWOnOff == "1":
            self.buttonMkrBW.setText("Marker %s Bandwidth [OFF]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe OFF" %active_marker)
            active_mkr_param[3] = 'OFF'
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif markerBWOnOff == "0":
            contOnOff = 0
            if active_mkr_param[4] == 'ON':
                active_mkr_param[4] = 'OFF'
                self.buttonNoiseMkr.setText("Noise Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[5] == 'ON':
                active_mkr_param[5] = 'OFF'
                self.buttonDeltaMkr.setText("Delta Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:DELTa:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[6] == 'ON':
                active_mkr_param[6] = 'OFF'
                self.buttonOSNRMkr.setText("OSNR Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            markerBWOnOff = '1'
            self.buttonMkrBW.setText("Marker %s Bandwidth [ON]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe ON" %active_marker)
            widget = InputDialog("Marker BW", "dB", str(active_BW_param[5]))
            widget.exec_()
            if widget.userInput != 0:
                active_BW_param[5] = widget.userInput
                bw = "CALC:MARK%s:FUNC:BAND:NDB " %active_marker + "%sdB" %widget.userInput
                active_mkr_param[3] = 'ON'
                self.updateMkrParam()
                self.setActMkr()
                instrument1.write(bw)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1BWCalc()
                        self.mkr1BWDisplay()
                    elif active_marker == '2':
                        self.mkr2BWCalc()
                        self.mkr2BWDisplay()
                    elif active_marker == '3':
                        self.mkr3BWCalc()
                        self.mkr3BWDisplay()
                    elif active_marker == '4':
                        self.mkr4BWCalc()
                        self.mkr4BWDisplay()
                    self.markerPlot()
                else:
                    reset = 1
                    contOnOff = 1
                    restartThread = 1
                
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            if restartThread == 1:
                self.sweepThreadOn()
        inUse = 0
        
    # Turn the noise marker on or off for the active marker       
    def noiseMkr(self):
        global noiseMarkOnOff
        global active_mkr_param
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        noiseMarkOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:NOISe:STATe?" %active_marker)).rstrip()
        if noiseMarkOnOff == "1":
            self.buttonNoiseMkr.setText("Noise Marker %s [OFF]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:STATe OFF" %active_marker)
            active_mkr_param[4] = 'OFF'
            self.updateMkrParam()
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif noiseMarkOnOff == "0":
            if active_mkr_param[3] == 'ON':
                active_mkr_param[3] = 'OFF'
                self.buttonMkrBW.setText("Marker %s Bandwidth [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[5] == 'ON':
                active_mkr_param[5] = 'OFF'
                self.buttonDeltaMkr.setText("Delta Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:DELTa:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[6] == 'ON':
                active_mkr_param[6] = 'OFF'
                self.buttonOSNRMkr.setText("OSNR Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            noiseMarkOnOff = '1'
            self.buttonNoiseMkr.setText("Noise Marker %s [ON]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:STATe ON" %active_marker)
            active_mkr_param[4] = 'ON'
            self.updateMkrParam()
            self.setActMkr()
            if repeatSweepOnOff == "0":
                if active_marker == '1':
                    self.mkr1NoiseDisplay()
                elif active_marker == '2':
                    self.mkr2NoiseDisplay()
                elif active_marker == '3':
                    self.mkr3NoiseDisplay()
                elif active_marker == '4':
                    self.mkr4NoiseDisplay()
                self.mkrCompDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
    
    # Turns the delta marker on or off for the active marker 
    def deltaMkr(self):
        global deltaMarkOnOff
        global active_mkr_param
        global delta_distance
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        restartThread = 0
        deltaMarkOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:DELTa:STATe?" %active_marker)).rstrip()
        if deltaMarkOnOff == "1":
            self.buttonDeltaMkr.setText("Delta Marker %s [OFF]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:DELTa:STATe OFF" %active_marker)
            active_mkr_param[5] = 'OFF'
            self.updateMkrParam()
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif deltaMarkOnOff == "0":
            contOnOff = 0
            if active_mkr_param[4] == 'ON':
                active_mkr_param[4] = 'OFF'
                self.buttonNoiseMkr.setText("Noise Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[3] == 'ON':
                active_mkr_param[3] = 'OFF'
                self.buttonMkrBW.setText("Marker %s Bandwidth [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[6] == 'ON':
                active_mkr_param[6] = 'OFF'
                self.buttonOSNRMkr.setText("OSNR Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            deltaMarkOnOff = '1'
            self.buttonDeltaMkr.setText("Delta Marker %s [ON]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:DELTa:STATe ON" %active_marker)
            widget = InputDialog("Delta Marker", "nm", '0')
            widget.exec_()
            if widget.userInput != 0:
                delta_distance = widget.userInput
                active_mkr_param[5] = 'ON'
                instrument1.write("CALC:MARK%s:FUNC:DELTa:X:OFFset %s%s" %(active_marker,delta_distance,wavelength_units))
                self.updateMkrParam()
                self.setActMkr()
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1DeltaCalc()
                        self.mkr1DeltaDisplay()
                    elif active_marker == '2':
                        self.mkr2DeltaCalc()
                        self.mkr2DeltaDisplay()
                    elif active_marker == '3':
                        self.mkr3DeltaCalc()
                        self.mkr3DeltaDisplay()
                    elif active_marker == '4':
                        self.mkr4DeltaCalc()
                        self.mkr4DeltaDisplay()
                    self.markerPlot()
                else:
                    reset = 1
                    contOnOff = 1
                    restartThread = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            if restartThread == 1:
                self.sweepThreadOn()
        inUse = 0
        
    # Turns the OSNR marker on or off for the active marker       
    def OSNRMkr(self):
        global osnrMarkOnOff
        global active_mkr_param
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        osnrMarkOnOff = str(instrument1.query("CALCulate:MARKer%s:FUNCtion:OSNR:STATe?" %active_marker)).rstrip()
        if osnrMarkOnOff == "1":
            self.buttonOSNRMkr.setText("OSNR Marker %s [OFF]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:STATe OFF" %active_marker)
            active_mkr_param[6] = 'OFF'
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        elif osnrMarkOnOff == "0":
            if active_mkr_param[4] == 'ON':
                active_mkr_param[4] = 'OFF'
                self.buttonNoiseMkr.setText("Noise Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[5] == 'ON':
                active_mkr_param[5] = 'OFF'
                self.buttonDeltaMkr.setText("Delta Marker %s [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:DELTa:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            if active_mkr_param[3] == 'ON':
                active_mkr_param[3] = 'OFF'
                self.buttonMkrBW.setText("Marker %s Bandwidth [OFF]" %active_marker)
                instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe OFF" %active_marker)
                if repeatSweepOnOff == "OFF":
                    if active_marker == '1':
                        self.mkr1ContDisplay()
                    elif active_marker == '2':
                        self.mkr2ContDisplay()
                    elif active_marker == '3':
                        self.mkr3ContDisplay()
                    elif active_marker == '4':
                        self.mkr4ContDisplay()
                    self.markerPlot()
                else:
                    reset = 1
            osnrMarkOnOff = '1'
            self.buttonOSNRMkr.setText("OSNR Marker %s [ON]" %active_marker)
            instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:STATe ON" %active_marker)
            active_mkr_param[6] = 'ON'
            self.updateMkrParam()
            self.setActMkr()
            if repeatSweepOnOff == "OFF":
                if active_marker == '1':
                    self.mkr1OSNRCalc()
                    self.mkr1OSNRDisplay()
                elif active_marker == '2':
                    self.mkr2OSNRCalc()
                    self.mkr2OSNRDisplay()
                elif active_marker == '3':
                    self.mkr3OSNRCalc()
                    self.mkr3OSNRDisplay()
                elif active_marker == '4':
                    self.mkr4OSNRCalc()
                    self.mkr4OSNRDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Further sub menu for line markers
    def lineMkrMenu(self):
        global lineMarkerOnOff
        global line1
        global line2
        global menuFlag
        menuFlag = 'lineMarkers'

        self.clearLayout(self.subButtonLayout)
        self.buttonWLLineMkr1 = QtWidgets.QPushButton("Wavelength Line Mkr 1", self)
        self.buttonWLLineMkr1.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonWLLineMkr1)
        self.buttonWLLineMkr2 = QtWidgets.QPushButton("Wavelength Line Mkr 2", self)
        self.buttonWLLineMkr2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonWLLineMkr2)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonLineMkrsOff = QtWidgets.QPushButton("Line Markers Off", self)
        self.buttonLineMkrsOff.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonLineMkrsOff)
        self.buttonAdvLineMkrFunc = QtWidgets.QPushButton("Advanved Line Marker Functions", self)
        self.buttonAdvLineMkrFunc.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonAdvLineMkrFunc)
        self.buttonPrevMenu = QtWidgets.QPushButton("Previous Menu", self)
        self.buttonPrevMenu.setMaximumSize(QtCore.QSize(250, 16777215))
        self.subButtonLayout.addWidget(self.buttonPrevMenu)

        if reset == 0:
            self.buttonWLLineMkr1.clicked.connect(self.WLLineMkr1)
            self.buttonWLLineMkr2.clicked.connect(self.WLLineMkr2)
            self.buttonLineMkrsOff.clicked.connect(self.lineMkrsOff)    
        else:
            self.buttonWLLineMkr1.clicked.connect(self.updatingException)
            self.buttonWLLineMkr2.clicked.connect(self.updatingException)
            self.buttonLineMkrsOff.clicked.connect(self.updatingException)
        self.buttonAdvLineMkrFunc.clicked.connect(self.advLineMkrFunc)
        self.buttonPrevMenu.clicked.connect(self.moreMkrFunc)

    def WLLineMkr1(self): 
        global line1
        global search_flag
        global sweep_flag
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global lineMarkerOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        Integration_Limit_1 = str(instrument1.query("CALCulate:TPOWer:IRANge:LOWer?")).rstrip()
        Integration_Limit_1 = str(conversions.str2float(Integration_Limit_1, wavelength_units))
        widget = InputDialog("Wavelenth Line Mkr 1", "%s" %wavelength_units, Integration_Limit_1)
        widget.exec_()
        if widget.userInput != 0:
            Integration_Limit_1 = str(widget.userInput).rstrip()
            line1 = Integration_Limit_1
            instrument1.write("CALCulate:TPOWer:IRANge:LOWer %s%s" %(Integration_Limit_1,wavelength_units))
            if search_flag == 1:
                instrument1.write("CALCulate:MARKer:SRANge:LOWer %s%s" %(Integration_Limit_1,wavelength_units))
            if sweep_flag == 1:
                instrument1.write("SENSe:WAVelength:SRANge:LOWer %s%s" %(Integration_Limit_1,wavelength_units))
            lineMarkerOnOff = 'On'
            self.linemarkerPlot()
            self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def WLLineMkr2(self):
        global line2
        global search_flag
        global sweep_flag
        global inUse
        global plotDone
        global reset
        global contOnOff
        global Integration_Limit_2
         
        global lineMarkerOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        Integration_Limit_2 = str(instrument1.query("CALCulate:TPOWer:IRANge:UPPer?")).rstrip()
        Integration_Limit_2 = str(conversions.str2float(Integration_Limit_2, wavelength_units))
        widget = InputDialog("Wavelenth Line Mkr 2", "%s" %wavelength_units, Integration_Limit_2)
        widget.exec_()
        if widget.userInput != 0:
            Integration_Limit_2 = str(widget.userInput).rstrip()
            line2 = Integration_Limit_2
            instrument1.write("CALCulate:TPOWer:IRANge:UPPer %s%s" %(Integration_Limit_2,wavelength_units))
            if search_flag == 1:
                instrument1.write("CALCulate:MARKer:SRANge:UPPer %s%s" %(Integration_Limit_1,wavelength_units))
            if sweep_flag == 1:
                instrument1.write("SENSe:WAVelength:SRANge:UPPer %s%s" %(Integration_Limit_1,wavelength_units))
            lineMarkerOnOff = 'On'
            self.linemarkerPlot()
            self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def lineMkrsOff(self):
        global sweep_limit
        global search_limit
        global integral_limit
        global trace_integral
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global lineMarkerOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")     
        instrument1.write("CALCulate:MARKer:SRANge OFF")
        instrument1.write("CALCulate:TPOWer:IRANge OFF")
        instrument1.write("SENSe:WAVelength:SRANge OFF")
        instrument1.write("CALCulate:TPOWer:STATe OFF")
        sweep_limit = 'Off'
        search_limit = 'Off'
        integral_limit = 'Off'
        trace_integral = 'Off'
        lineMarkerOnOff = 'Off'
        self.linemarkerPlot()
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Brings up window for advanced line marker functions
    def advLineMkrFunc(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global lineMarkerOnOff
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        widget = AdvancedLineMarkerWindow()
        widget.exec_()
        self.linemarkerPlot()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0


    # Trace sub-menu
    def tracesMenu(self):
        global menuFlag
        menuFlag = 'traces' # Allows redraw to this menu if a different trace is made active

        self.clearLayout(self.subButtonLayout)
        self.buttonUpdtTrce = QtWidgets.QPushButton("Update Trace %s [%s]" %(active_trace[2], active_trace_param[0]), self)
        self.buttonViewTrce = QtWidgets.QPushButton("View Trace %s [%s]" %(active_trace[2],active_trace_param[1]), self)
        self.buttonHoldTrce = QtWidgets.QPushButton("Hold Trace %s [%s]" %(active_trace[2],active_trace_param[2]), self)
        self.buttonAveraging = QtWidgets.QPushButton("Averaging %s [%s]" %(active_trace[2],active_trace_param[3]), self)
        if reset == 0:
            self.menuUpdtTrce = QtWidgets.QMenu()
            self.menuUpdtTrce.addAction("On", self.UpdtTrceAction1)
            self.menuUpdtTrce.addAction("Off", self.UpdtTrceAction2)
            self.buttonUpdtTrce.setMenu(self.menuUpdtTrce)
            self.menuViewTrce = QtWidgets.QMenu()
            self.menuViewTrce.addAction("On", self.ViewTrceAction1)
            self.menuViewTrce.addAction("Off", self.ViewTrceAction2)
            self.buttonViewTrce.setMenu(self.menuViewTrce)
            self.menuHoldTrce = QtWidgets.QMenu()
            self.menuHoldTrce.addAction("None", self.HoldTrceAction1)
            self.menuHoldTrce.addAction("Min", self.HoldTrceAction2)
            self.menuHoldTrce.addAction("Max", self.HoldTrceAction3)
            self.buttonHoldTrce.setMenu(self.menuHoldTrce)
            self.menuAveraging = QtWidgets.QMenu()
            self.menuAveraging.addAction("On", self.AveragingAction1)
            self.menuAveraging.addAction("Off", self.AveragingAction2)
            self.buttonAveraging.setMenu(self.menuAveraging)
        else:
            self.buttonUpdtTrce.clicked.connect(self.updatingException)
            self.buttonViewTrce.clicked.connect(self.updatingException)
            self.buttonHoldTrce.clicked.connect(self.updatingException)
            self.buttonAveraging.clicked.connect(self.updatingException)
        self.buttonUpdtTrce.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonUpdtTrce)
        self.buttonViewTrce.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonViewTrce)
        self.buttonHoldTrce.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonHoldTrce)
        self.buttonAveraging.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonAveraging)
        self.buttonTrceMath = QtWidgets.QPushButton("Trace Math", self)
        self.buttonTrceMath.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonTrceMath)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonTrceSetup = QtWidgets.QPushButton("Trace Setup", self)
        self.buttonTrceSetup.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonTrceSetup)

        if reset == 0:
            self.buttonTrceMath.clicked.connect(self.trceMath)
            self.buttonTrceSetup.clicked.connect(self.trceSetup)
        else:
            self.buttonTrceMath.clicked.connect(self.updatingException)
            self.buttonTrceSetup.clicked.connect(self.updatingException)

    def UpdtTrceAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonUpdtTrce.setText("Update Trace %s [ON]" %active_trace[2])
        instrument1.write("TRACe:FEED:CONTrol %s,ALW" %active_trace)
        active_trace_param[0] = 'ON'
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def UpdtTrceAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonUpdtTrce.setText("Update Trace %s [OFF]" %active_trace[2])
        instrument1.write("TRACe:FEED:CONTrol %s,NEV" %active_trace)
        active_trace_param[0] = 'OFF'
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ViewTrceAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonViewTrce.setText("View Trace %s [ON]" %active_trace[2])
        instrument1.write("DISPlay:WINDow:TRACe:STATe %s,ON" %active_trace)
        active_trace_param[1] = "ON"
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ViewTrceAction2(self): 
        global TRA_plot
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonViewTrce.setText("View Trace %s [OFF]" %active_trace[2])
        instrument1.write("DISPlay:WINDow:TRACe:STATe %s,OFF" %active_trace)
        active_trace_param[1] = "OFF"
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            if active_trace == "TRA":
                self.p1.removeItem(TRA_plot)
            if active_trace == "TRB":
                self.p1.removeItem(TRB_plot)
            if active_trace == "TRC":
                self.p1.removeItem(TRC_plot)
            if active_trace == "TRD":
                self.p1.removeItem(TRD_plot)
            if active_trace == "TRE":
                self.p1.removeItem(TRE_plot)
            if active_trace == "TRF":
                self.p1.removeItem(TRF_plot)
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")

        inUse = 0
            
    def HoldTrceAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonHoldTrce.setText("Hold Trace %s [NONE]" %active_trace[2])
        instrument1.write("CALCulate%s:MAXimum:STATe OFF" %active_trace_num)
        instrument1.write("CALCulate%s:MINimum:STATe OFF" %active_trace_num)
        active_trace_param[2] = 'NONE'
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def HoldTrceAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonHoldTrce.setText("Hold Trace %s [MIN]" %active_trace[2])
        instrument1.write("CALCulate%s:MINimum:STATe ON" %active_trace_num)
        active_trace_param[2] = 'MIN'
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def HoldTrceAction3(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonHoldTrce.setText("Hold Trace %s [MAX]" %active_trace[2])
        instrument1.write("CALCulate%s:MAXimum:STATe ON" %active_trace_num)
        active_trace_param[2] = 'MAX'
        self.updateTrcParam()
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    # Sub menu for trace math
    def trceMath(self):
        global menuFlag
        menuFlag = 'traceMath'
        
        self.clearLayout(self.subButtonLayout)
        self.buttonDefMathTrcC = QtWidgets.QPushButton("Default Math Trace C", self)
        self.buttonDefMathTrcF = QtWidgets.QPushButton("Default Math Trace F", self)
        self.buttonExchMenu = QtWidgets.QPushButton("Exchange Menu", self)
        if reset == 0:
            self.menuTrcMathC = QtWidgets.QMenu()
            self.menuTrcMathC.addAction("Log: C = A-B", self.TrcMathCAction1)
            self.menuTrcMathC.addAction("Log: C = A+B", self.TrcMathCAction2)
            self.menuTrcMathC.addAction("Lin: C = A-B", self.TrcMathCAction3)
            self.menuTrcMathC.addAction("Lin: C = A+B", self.TrcMathCAction4)
            self.menuTrcMathC.addAction("Trace C Math Off", self.TrcMathCAction5)
            self.buttonDefMathTrcC.setMenu(self.menuTrcMathC)
            self.menuTrcMathF = QtWidgets.QMenu()
            self.menuTrcMathF.addAction("Log: F = C-D", self.TrcMathFAction1)
            self.menuTrcMathF.addAction("Trace F Math Off", self.TrcMathFAction2)
            self.buttonDefMathTrcF.setMenu(self.menuTrcMathF)
            self.menuExchange = QtWidgets.QMenu()
            self.menuExchange.addAction("A Exchange B", self.ExchangeAction1)
            self.menuExchange.addAction("B Exchange C", self.ExchangeAction2)
            self.menuExchange.addAction("C Exchange A", self.ExchangeAction3)
            self.menuExchange.addAction("D Exchange A", self.ExchangeAction4)
            self.menuExchange.addAction("E Exchange A", self.ExchangeAction5)
            self.menuExchange.addAction("F Exchange A", self.ExchangeAction6)
            self.buttonExchMenu.setMenu(self.menuExchange)
        else:
            self.buttonDefMathTrcC.clicked.connect(self.updatingException)
            self.buttonDefMathTrcF.clicked.connect(self.updatingException)
            self.buttonExchMenu.clicked.connect(self.updatingException)
        self.buttonDefMathTrcC.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonDefMathTrcC)
        self.buttonDefMathTrcF.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonDefMathTrcF)
        self.buttonExchMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonExchMenu)
        self.buttonTrceOffset = QtWidgets.QPushButton("Trace Offset", self)
        self.buttonTrceOffset.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonTrceOffset)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonAllMathOff = QtWidgets.QPushButton("All Math Off", self)
        self.buttonAllMathOff.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonAllMathOff)
        self.buttonPrevMenu = QtWidgets.QPushButton("Previous Menu", self)
        self.buttonPrevMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPrevMenu)

        if reset == 0:
            self.buttonTrceOffset.clicked.connect(self.trceOffset)
            self.buttonAllMathOff.clicked.connect(self.allMathOff)
        else:
            self.buttonTrceOffset.clicked.connect(self.updatingException)
            self.buttonAllMathOff.clicked.connect(self.updatingException)
        self.buttonPrevMenu.clicked.connect(self.tracesMenu)

    def TrcMathCAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate3:MATH:STATe ON")
        instrument1.write("CALCulate3:MATH:EXPRession (TRA / TRB)")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TrcMathCAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate3:MATH:STATe ON")
        instrument1.write("CALCulate3:MATH:EXPRession (TRA * TRB)")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        

    def TrcMathCAction3(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate3:MATH:STATe ON")
        instrument1.write("CALCulate3:MATH:EXPRession (TRA - TRB)")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TrcMathCAction4(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate3:MATH:STATe ON")
        instrument1.write("CALCulate3:MATH:EXPRession (TRA + TRB)")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TrcMathCAction5(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate3:MATH:STATe OFF")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TrcMathFAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate6:MATH:STATe ON")
        instrument1.write("CALCulate6:MATH:EXPRession (TRC / TRD)")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TrcMathFAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate6:MATH:STATe OFF")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    # The exchange actions swap traces with each other
    def ExchangeAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("TRACe:EXCHange TRA,TRB")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ExchangeAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("TRACe:EXCHange TRB,TRC")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ExchangeAction3(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("TRACe:EXCHange TRC,TRA")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ExchangeAction4(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("TRACe:EXCHange TRD,TRA")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ExchangeAction5(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("TRACe:EXCHange TRE,TRA")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ExchangeAction6(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("TRACe:EXCHange TRF,TRA")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def trceOffset(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        Trace_Offset = str(instrument1.query("CALCulate%s:OFFSet?" %active_trace_num)).rstrip()
        Trace_Offset = str(conversions.str2float(Trace_Offset, amplitude_units))
        widget = InputDialog("Trace %s Offset" %active_trace[2], "%s" %amplitude_units, Trace_Offset)
        widget.exec_()
        if widget.userInput != 0:
            Trace_Offset = str(widget.userInput).rstrip()
            instrument1.write("CALCulate%s:OFFSet %s" %(active_trace_num, Trace_Offset))
            if repeatSweepOnOff == "OFF":
                sweep = 1
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
            
    def allMathOff(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        instrument1.write("CALCulate3:MATH:STATe OFF")
        instrument1.write("CALCulate6:MATH:STATe OFF")
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def AveragingAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        self.buttonAveraging.setText("Averaging [ON]")
        instrument1.write("CALCulate:AVERage:STATe ON")
        active_trace_param[3] = "ON"
        av_count = instrument1.query("CALCulate:AVERage:COUNt?")
        widget = InputDialog("Average Count", "Average Count", av_count)
        widget.exec_()
        if widget.userInput != 0:
            av_count = str(widget.userInput).rstrip()
            instrument1.write("CALCulate:AVERage:COUNt %s" %av_count)
        self.updateTrcParam()
        self.infoDisplay()
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0

    def AveragingAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonAveraging.setText("Averaging [OFF]")
        instrument1.write("CALCulate:AVERage:STATe OFF")
        active_trace_param[3] = "OFF"
        self.updateTrcParam()
        self.infoDisplay()
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def trceSetup(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        num_points = str(instrument1.query("SENSe:SWEep:POINts?")).rstrip()
        widget = InputDialog("Trace Setup", "Sweep Points", num_points[1:5])
        widget.exec_()
        if widget.userInput != 0:
            num_points = "SENSe:SWEep:POINts " + "%s" %widget.userInput
            instrument1.write(num_points)
            num_points = widget.userInput
            if repeatSweepOnOff == "OFF":
                sweep = 0
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        

    # Bandwidth/Sweep sub-menu
    def bwMenu(self):
        global repeatSweepOnOff
        global menuFlag
        menuFlag = 'bandwidth'
        
        self.clearLayout(self.subButtonLayout)    
        self.buttonResBW = QtWidgets.QPushButton("Res BW [%s]" %resBwManAuto, self)
        self.buttonVidBW = QtWidgets.QPushButton("Video BW [%s]" %vidBwManAuto, self)
        self.buttonSweepTime = QtWidgets.QPushButton("Sweep Time [%s]" %sweepTimeManAuto, self)
        self.buttonRptSweep = QtWidgets.QPushButton("Repeat Sweep [%s]" %repeatSweepOnOff, self)
        if reset == 0:
            self.menuResBw = QtWidgets.QMenu()
            self.menuResBw.addAction("Auto", self.ResBWAction1)
            self.menuResBw.addAction("Manual", self.ResBWAction2)
            self.buttonResBW.setMenu(self.menuResBw)
            self.menuVidBW = QtWidgets.QMenu()
            self.menuVidBW.addAction("Auto", self.VidBWAction1)
            self.menuVidBW.addAction("Manual", self.VidBWAction2)
            self.buttonVidBW.setMenu(self.menuVidBW)                    
            self.menuSweepTime = QtWidgets.QMenu()
            self.menuSweepTime.addAction("Auto", self.SweepTimeAction1)
            self.menuSweepTime.addAction("Manual", self.SweepTimeAction2)
            self.buttonSweepTime.setMenu(self.menuSweepTime)                    
            self.menuRptSweep = QtWidgets.QMenu()
            self.menuRptSweep.addAction("On", self.RptSweepAction1)
            self.menuRptSweep.addAction("Off", self.RptSweepAction2)
            self.buttonRptSweep.setMenu(self.menuRptSweep)
        else:
            self.buttonResBW.clicked.connect(self.updatingException)
            self.buttonVidBW.clicked.connect(self.updatingException)
            self.buttonSweepTime.clicked.connect(self.updatingException)
            self.buttonRptSweep.clicked.connect(self.updatingException)
        self.buttonResBW.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonResBW)
        self.buttonVidBW.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonVidBW)
        self.buttonSweepTime.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonSweepTime)
        self.buttonRptSweep.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonRptSweep)
        self.buttonSnglSweep = QtWidgets.QPushButton("Single Sweep", self)
        self.buttonSnglSweep.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonSnglSweep)
        self.buttonBlank = QtWidgets.QPushButton("", self)
        self.buttonBlank.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonBlank)
        self.buttonMoreBWFunc = QtWidgets.QPushButton("More BW/Sweep Functions", self)
        self.buttonMoreBWFunc.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonMoreBWFunc)

        if reset == 0:
            self.buttonSnglSweep.clicked.connect(self.snglSweep)
            self.buttonMoreBWFunc.clicked.connect(self.moreBWFunc)
        else:
            self.buttonSnglSweep.clicked.connect(self.updatingException)
            self.buttonMoreBWFunc.clicked.connect(self.updatingException)

    def ResBWAction1(self):
        global resBwManAuto
        global resBw
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonResBW.setText("Res BW [AUTO]")
        instrument1.write("SENSe:BANDwidth:RESolution:AUTO 1")
        resBwManAuto = "AUTO"
        resBw = conversions.str2float(instrument1.query("SENSe:BANDwidth:RESolution?").rstrip(),wavelength_units)
        self.infoDisplay()
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ResBWAction2(self):
        global resBwManAuto
        global resBw
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        resBw = conversions.str2float(instrument1.query("SENSe:BANDwidth:RESolution?").rstrip(),wavelength_units)
        widget = InputDialog("Res BW", "%s" %wavelength_units, str(resBw))
        widget.exec_()
        if widget.userInput != 0:
            self.buttonResBW.setText("Res BW [MAN]")
            bandwidth = "SENSe:BANDwidth:RESolution " + "%s%s" %(widget.userInput,wavelength_units)
            instrument1.write(bandwidth)
            sweep = 1
            resBwManAuto = "MAN"
            resBw = conversions.str2float(instrument1.query("SENSe:BANDwidth:RESolution?").rstrip(),wavelength_units)
            self.infoDisplay()
            if repeatSweepOnOff == "OFF":
                sweep = 1
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0

    def VidBWAction1(self):
        global vidBwManAuto
        global vidBw
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonVidBW.setText("Video BW [AUTO]")
        instrument1.write("SENSe:BANDwidth:VIDeo:AUTO 1")
        vidBwManAuto = "AUTO"
        vidBw = conversions.str2float(instrument1.query("SENSe:BANDwidth:VIDeo?").rstrip(), frequency_units)
        self.infoDisplay()
        if repeatSweepOnOff == "OFF":
            sweep = 1
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                         trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                         trace_d_param, trace_e_param, trace_f_param, sweep)
            if active_marker == '1':
                self.mkr1ContDisplay()
            elif active_marker == '2':
                self.mkr2ContDisplay()
            elif active_marker == '3':
                self.mkr3ContDisplay()
            elif active_marker == '4':
                self.mkr4ContDisplay()
            self.markerPlot()
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def VidBWAction2(self):
        global vidBwManAuto
        global vidBw
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        vidBw = conversions.str2float(instrument1.query("SENSe:BANDwidth:VIDeo?").rstrip(),'kHz')
        widget = InputDialog("Video BW", "%s" %frequency_units, str(vidBw))
        widget.exec_()
        if widget.userInput != 0:
            vidBwManAuto = "MAN"
            self.buttonVidBW.setText("Video BW [MAN]")
            bandwidth = "SENSe:BANDwidth:VIDeo " + "%s%s" %(widget.userInput,frequency_units) #may be wrong unit
            instrument1.write(bandwidth)
            vidBw = conversions.str2float(widget.userInput,frequency_units)
            if repeatSweepOnOff == "OFF":
                sweep = 1
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def SweepTimeAction1(self):
        global sweepTimeManAuto
        global sweepTime
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonSweepTime.setText("Sweep Time [AUTO]")
        instrument1.write("SENSe:SWEep:TIME:AUTO 1")
        sweepTimeManAuto = "AUTO"
        sweepTime = float(instrument1.query("SENSe:SWEep:TIME?"))
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def SweepTimeAction2(self):
        global sweepTimeManAuto
        global sweepTime
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        sweepTime = float(instrument1.query("SENSe:SWEep:TIME?"))
        widget = InputDialog("Sweep Time", "s", str(sweepTime))
        widget.exec_()
        if widget.userInput != 0:
            sweepTimeManAuto = "MAN"
            self.buttonSweepTime.setText("Sweep Time [MAN]")
            stime = "SENSe:SWEep:TIME " + "%ss" %widget.userInput
            instrument1.write(stime)
            sweepTime = conversions.str2float(widget.userInput,time_units)
            if repeatSweepOnOff == "OFF":
                sweep = 1
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
                if active_marker == '1':
                    self.mkr1ContDisplay()
                elif active_marker == '2':
                    self.mkr2ContDisplay()
                elif active_marker == '3':
                    self.mkr3ContDisplay()
                elif active_marker == '4':
                    self.mkr4ContDisplay()
                self.markerPlot()
            else:
                reset = 1
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0

    def RptSweepAction1(self): 
        global repeatSweepOnOff
        global contOnOff
        global reset
        contOnOff = 1
        reset = 1
        self.buttonRptSweep.setText("Repeat Sweep [ON]")
        instrument1.write("INITiate:CONTinuous 1")
        repeatSweepOnOff = "ON"
        self.sweepThreadOn()
        
    def RptSweepAction2(self):
        global repeatSweepOnOff
        global contOnOff
        contOnOff = 0
        self.buttonRptSweep.setText("Repeat Sweep [OFF]")
        repeatSweepOnOff = "OFF"
        while plotDone == 0:
            pass
        if mkr_1_param[0] == '1':
            instrument1.write("CALCulate:MARKer1:X %s%s" %(mkr_1_param[1],mkr_units))
        if mkr_2_param[0] == '1':
            instrument1.write("CALCulate:MARKer2:X %s%s" %(mkr_2_param[1],mkr_units))
        if mkr_3_param[0] == '1':
            instrument1.write("CALCulate:MARKer3:X %s%s" %(mkr_3_param[1],mkr_units))
        if mkr_4_param[0] == '1':
            instrument1.write("CALCulate:MARKer4:X %s%s" %(mkr_4_param[1],mkr_units))
        self.snglSweep()
        
       
    def snglSweep(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        sweep = 1
        self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                     trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                     trace_d_param, trace_e_param, trace_f_param, sweep)
        if active_marker == '1':
            self.mkr1ContDisplay()
        elif active_marker == '2':
            self.mkr2ContDisplay()
        elif active_marker == '3':
            self.mkr3ContDisplay()
        elif active_marker == '4':
            self.mkr4ContDisplay()
        self.markerPlot()
        self.infoDisplay()
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    # Sub menu for more bandwidth functions
    # NOTE: Gated mode available on machine is not available as a remote function
    def moreBWFunc(self):
        global menuFlag
        menuFlag = 'moreBandwidth'
        
        self.clearLayout(self.subButtonLayout)    
        self.buttonTrigMode = QtWidgets.QPushButton("Trigger Mode [%s]" %Trigger_Mode, self)
        self.buttonADCTrigSync = QtWidgets.QPushButton("ADC Trig Sync [%s]" %trigSyncLowHighPulse, self)
        self.buttonADCSyncOut = QtWidgets.QPushButton("ADC Sync Out [%s]" %syncOutOnOff, self)
        if reset == 0:
            if repeatSweepOnOff == "ON":
                self.buttonTrigMode.clicked.connect(self.sweepException)
            else:
                self.menuTrigMode = QtWidgets.QMenu()
                self.menuTrigMode.addAction("Internal", self.TrigModeAction1)
                self.menuTrigMode.addAction("External", self.TrigModeAction3)
                self.menuTrigMode.addAction("ADC+", self.TrigModeAction4)
                self.menuTrigMode.addAction("ADC-", self.TrigModeAction5)
                self.menuTrigMode.addAction("ADC AC", self.TrigModeAction6)
                self.buttonTrigMode.setMenu(self.menuTrigMode)
            self.menuADCTrig = QtWidgets.QMenu()
            self.menuADCTrig.addAction("Low", self.ADCTrigAction1)
            self.menuADCTrig.addAction("High", self.ADCTrigAction2)
            self.menuADCTrig.addAction("Pulse", self.ADCTrigAction3)
            self.buttonADCTrigSync.setMenu(self.menuADCTrig)
        else:
            self.buttonTrigMode.clicked.connect(self.updatingException)
            self.buttonADCTrigSync.clicked.connect(self.updatingException)
        self.buttonTrigMode.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonTrigMode)
        self.buttonTrigDelay = QtWidgets.QPushButton("Trigger Delay", self)
        self.buttonTrigDelay.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonTrigDelay)
        self.buttonADCTrigSync.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonADCTrigSync)
        self.buttonADCSyncOut.setCheckable(1)
        self.buttonADCSyncOut.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonADCSyncOut)
        self.buttonADCSyncOutDuty = QtWidgets.QPushButton("ADC Sync Out Duty Cycle", self)
        self.buttonADCSyncOutDuty.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonADCSyncOutDuty)
        self.buttonADCSyncOutPulse = QtWidgets.QPushButton("ADC Sync Out Pulse Width", self)
        self.buttonADCSyncOutPulse.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonADCSyncOutPulse)
        self.buttonPrevMenu = QtWidgets.QPushButton("Previous Menu", self)
        self.buttonPrevMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.subButtonLayout.addWidget(self.buttonPrevMenu)

        if reset == 0:
            self.buttonTrigDelay.clicked.connect(self.trigDelay)
            self.buttonADCSyncOut.clicked.connect(self.ADCSyncOut)
            self.buttonADCSyncOutDuty.clicked.connect(self.ADCSyncOutDuty)
            self.buttonADCSyncOutPulse.clicked.connect(self.ADCSyncOutPulse)
        else:
            self.buttonTrigDelay.clicked.connect(self.updatingException)
            self.buttonADCSyncOut.clicked.connect(self.updatingException)
            self.buttonADCSyncOutDuty.clicked.connect(self.updatingException)
            self.buttonADCSyncOutPulse.clicked.connect(self.updatingException)
        self.buttonPrevMenu.clicked.connect(self.bwMenu)

    def TrigModeAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global Trigger_Mode
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTrigMode.setText("Trigger Mode [Internal]")
        Trigger_Mode = "Internal"
        instrument1.write("TRIGger:SOURce INT")
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def TrigModeAction3(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global Trigger_Mode
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTrigMode.setText("Trigger Mode [External]")
        Trigger_Mode = "External"
        instrument1.write("TRIGger:SOURce EXT")
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def TrigModeAction4(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global Trigger_Mode
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTrigMode.setText("Trigger Mode [ADC+]")
        Trigger_Mode = "ADC+"
        instrument1.write("TRIGger:SLOPe POS")
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def TrigModeAction5(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global Trigger_Mode
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTrigMode.setText("Trigger Mode [ADC-]")
        Trigger_Mode = "ADC-"
        instrument1.write("TRIGger:SLOPe NEG")
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def TrigModeAction6(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        global Trigger_Mode
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonTrigMode.setText("Trigger Mode [ADC AC]")
        Trigger_Mode = "ADC AC"
        instrument1.write("TRIGger:SLOPe EITH")
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def trigDelay(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("TRIGger:DELay?")
        current_value = str(conversions.str2float(value,"us")) 
        widget = InputDialog("Trigger Delay", "us", current_value)
        widget.exec_()
        if widget.userInput != 0:
            delay = "TRIGger:DELay " + "%sus" %widget.userInput
            instrument1.write(delay)
            if repeatSweepOnOff == "OFF":
                sweep = 0
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def ADCTrigAction1(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global trigSyncLowHighPulse
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonADCTrigSync.setText("ADC Trig Sync [LOW]")
        trigSyncLowHighPulse = "LOW"
        instrument1.write("TRIGger:OUTPut OFF")
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ADCTrigAction2(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global trigSyncLowHighPulse
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonADCTrigSync.setText("ADC Trig Sync [HIGH]")
        instrument1.write("TRIGger:OUTPut ON")
        trigSyncLowHighPulse = "HIGH"
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ADCTrigAction3(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global trigSyncLowHighPulse
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        self.buttonADCTrigSync.setText("ADC Trig Sync [PULSE]")
        trigSyncLowHighPulse = "PULSE"
        instrument1.write("TRIGger:OUTPut AUTO")
        if repeatSweepOnOff == "OFF":
            sweep = 0
            self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
        else:
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0

    def ADCSyncOut(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
        global syncOutOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
        syncOutOnOff = str(instrument1.query("TRIGger:OUTPut:PULSe:STATe?")).rstrip()
        if syncOutOnOff == "0":
            self.buttonADCSyncOut.setText("ADC Sync Out [ON]")
            instrument1.write("TRIGger:OUTPut:PULSe:STATe 1")
            syncOutOnOff = "ON"
            if repeatSweepOnOff == "OFF":
                sweep = 0
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
        elif syncOutOnOff == "1":
            self.buttonADCSyncOut.setText("ADC Sync Out [OFF]")
            instrument1.write("TRIGger:OUTPut:PULSe:STATe 0")
            syncOutOnOff = "OFF"
            if repeatSweepOnOff == "OFF":
                sweep = 0
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
        if repeatSweepOnOff == "ON":
            reset = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
        inUse = 0
        
    def ADCSyncOutDuty(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = float(instrument1.query("TRIGger:OUTPut:PULSe:DCYCle?"))
        widget = InputDialog("ADC Sync Out Duty Cycle", "%", str(value))
        widget.exec_()
        if widget.userInput != 0:
            duty_cycle = "TRIGger:OUTPut:PULSe:DCYCle " + "%s" %widget.userInput
            instrument1.write(duty_cycle)
            if repeatSweepOnOff == "OFF":
                sweep = 0
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0
        
    def ADCSyncOutPulse(self):
        global inUse
        global plotDone
        global reset
        global contOnOff
         
        inUse = 1
        
        if repeatSweepOnOff == "ON":
            while plotDone == 0:
                pass
            instrument1.write("INITiate:CONTinuous 0")
            contOnOff = 0
        value = instrument1.query("TRIGger:OUTPut:PULSe:WIDTh?")
        current_value = str(conversions.str2float(value,"us")) 
        widget = InputDialog("ADC Sync Out Pulse Width", "us", current_value)
        widget.exec_()
        if widget.userInput != 0:
            pulse_width = "TRIGger:OUTPut:PULSe:WIDTh " + "%sus" %widget.userInput
            instrument1.write(pulse_width)
            if repeatSweepOnOff == "OFF":
                sweep = 0
                self.traceDisplay( num_points, active_trace, wavelength_name, amplitude_name, wavelength_units_display, amplitude_units,
                             trace_a_data, trace_b_data, trace_c_data, trace_d_data, trace_e_data, trace_f_data, trace_a_param, trace_b_param, trace_c_param,
                             trace_d_param, trace_e_param, trace_f_param, sweep)
            else:
                reset = 1
        if repeatSweepOnOff == "ON":
            contOnOff = 1
            self.goToMenu()
            instrument1.write("INITiate:CONTinuous 1")
            self.sweepThreadOn()
        inUse = 0

## ------------------------------------------------------
##      CLASSES FOR OTHER WINDOWS
## ------------------------------------------------------

# The input dialog class is used throught the agilent class to allow the
# user to input values into menu options
class InputDialog(QtWidgets.QDialog, Ui_inputDialog):
    def __init__(self, title, unit, value, parent=None):
        super(InputDialog, self).__init__(parent)
        global flag
        self.setupUi(self)
        self.setWindowTitle(title)
        self.label.setText(unit)
        self.lineEdit.setText(value)
        validator = QtGui.QDoubleValidator()
        self.lineEdit.setValidator(validator)
        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)
        flag = 0

    def onAccept(self):
        global flag
        self.userInput = self.lineEdit.text()
        flag = 1
        return self.userInput
        
    def onReject(self):
        global flag
        self.userInput = 0
        flag = 1
        return self.userInput

class ExceptionDialog(QtWidgets.QDialog, Ui_exceptionDialog):
    def __init__(self, message, parent=None):
        super(ExceptionDialog, self).__init__(parent)
        self.setupUi(self)
        self.label.setText(message)
        self.accepted.connect(self.onAccept)

    def onAccept(self):
        return

# The confirm dialog class is used twice to check if the user really wants to automeasure or autoalign
class ConfirmDialog(QtWidgets.QDialog, Ui_confirmDialog):
    def __init__(self, title, parent=None):
        super(ConfirmDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def onAccept(self):
        self.userInput = 1
        return self.userInput
        
    def onReject(self):
        self.userInput = 0
        return self.userInput
    
# Window to select which markers are displayed at any given time
class ActiveMarkersWindow(QtWidgets.QDialog, Ui_activeMarkersWindow):
    def __init__(self, parent=None):
        super(ActiveMarkersWindow, self).__init__(parent)
        self.setupUi(self)
        if float(instrument1.query("CALCulate:MARKer1:STATe?")) == 1:
            self.checkMkr1.setChecked(True)
        if float(instrument1.query("CALCulate:MARKer2:STATe?")) == 1:
            self.checkMkr2.setChecked(True)
        if float(instrument1.query("CALCulate:MARKer3:STATe?")) == 1:
            self.checkMkr3.setChecked(True)
        if float(instrument1.query("CALCulate:MARKer4:STATe?")) == 1:
            self.checkMkr4.setChecked(True)

        self.buttonAllOff.clicked.connect(self.allMkrsOff)
        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def allMkrsOff(self):
        self.checkMkr1.setChecked(False)
        self.checkMkr2.setChecked(False)
        self.checkMkr3.setChecked(False)
        self.checkMkr4.setChecked(False)

    def onAccept(self):
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param
        
        if self.checkMkr1.isChecked() == True:
            trc = mkr_1_param[7]
            instrument1.write("CALCulate:MARKer1:STATe ON")
            instrument1.write("CALCulate:MARKer1:TRACe %s" %trc)
            mkr_1_param[0] = "1"
        if self.checkMkr1.isChecked() == False:
            instrument1.write("CALCulate:MARKer1:STATe OFF")
            mkr_1_param[0] = "0"
            mkr_1_param[3] = 'OFF'
            mkr_1_param[4] = 'OFF'
            mkr_1_param[5] = 'OFF'
            mkr_1_param[6] = 'OFF'
        if self.checkMkr2.isChecked() == True:
            trc = mkr_2_param[7]
            instrument1.write("CALCulate:MARKer2:STATe ON")
            instrument1.write("CALCulate:MARKer2:TRACe %s" %trc)
            mkr_2_param[0] = "1"
        if self.checkMkr2.isChecked() == False:
            instrument1.write("CALCulate:MARKer2:STATe OFF")
            mkr_2_param[0] = "0"
            mkr_2_param[3] = 'OFF'
            mkr_2_param[4] = 'OFF'
            mkr_2_param[5] = 'OFF'
            mkr_2_param[6] = 'OFF'
        if self.checkMkr3.isChecked() == True:
            trc = mkr_3_param[7]
            instrument1.write("CALCulate:MARKer3:STATe ON")
            instrument1.write("CALCulate:MARKer3:TRACe %s" %trc)
            mkr_3_param[0] = "1"
        if self.checkMkr3.isChecked() == False:
            instrument1.write("CALCulate:MARKer3:STATe OFF")
            mkr_3_param[0] = "0"
            mkr_3_param[3] = 'OFF'
            mkr_3_param[4] = 'OFF'
            mkr_3_param[5] = 'OFF'
            mkr_3_param[6] = 'OFF'
        if self.checkMkr4.isChecked() == True:
            trc = mkr_4_param[7]
            instrument1.write("CALCulate:MARKer4:STATe ON")
            instrument1.write("CALCulate:MARKer4:TRACe %s" %trc)
            mkr_4_param[0] = "1"
        if self.checkMkr4.isChecked() == False:
            instrument1.write("CALCulate:MARKer4:STATe OFF")
            mkr_4_param[0] = "0"
            mkr_4_param[3] = 'OFF'
            mkr_4_param[4] = 'OFF'
            mkr_4_param[5] = 'OFF'
            mkr_4_param[6] = 'OFF'

        global active_marker
        if mkr_1_param[0] == '1':
            active_marker = '1'
        if mkr_2_param[0] == '1':
            active_marker = '2'
        if mkr_3_param[0] == '1':
            active_marker = '3'
        if mkr_4_param[0] == '1':
            active_marker = '4'

        self.markerReturn = 1
        return self.markerReturn

    def onReject(self):
        self.markerReturn = 0
        return self.markerReturn

# Window to change amplitude setup parameters (global)
class AmplitudeSetup(QtWidgets.QDialog, Ui_amplitudeSetupWindow):
    def __init__(self, parent=None):
        super(AmplitudeSetup, self).__init__(parent)
        self.setupUi(self)
        global auto_ranging
        global auto_zero
        global auto_chop
        global amplitude_correction_mode
        
        if amplitude_units == 'dB':
            amp_units_display = 'Auto'
        else:
            amp_units_display = 'W'
        self.buttonAmpUnits.setText("%s" %amp_units_display)
        self.menuAmpUnits = QtWidgets.QMenu()
        self.menuAmpUnits.addAction("Auto", self.AmpUnitsAction1)
        self.menuAmpUnits.addAction("W", self.AmpUnitsAction2)
        self.buttonAmpUnits.setMenu(self.menuAmpUnits)
        if auto_ranging == '1':
            auto_range_display = 'On'
        elif auto_ranging == '0':
            auto_range_display = 'Off'
        self.buttonAutoRang.setText("%s" %auto_range_display)
        self.menuAutoRang = QtWidgets.QMenu()
        self.menuAutoRang.addAction("On", self.AutoRangAction1)
        self.menuAutoRang.addAction("Off", self.AutoRangAction2)
        self.buttonAutoRang.setMenu(self.menuAutoRang)
        if auto_zero == '1':
            auto_zero_display = 'On'
        elif auto_zero == '0':
            auto_zero_display = 'Off'
        self.buttonAutoZero.setText("%s" %auto_zero_display)
        self.menuAutoZero = QtWidgets.QMenu()
        self.menuAutoZero.addAction("On", self.AutoZeroAction1)
        self.menuAutoZero.addAction("Off", self.AutoZeroAction2)
        if auto_chop == '1':
            auto_chop_display = 'On'
        elif auto_chop == '0':
            auto_chop_display = 'Off'
        self.buttonAutoZero.setMenu(self.menuAutoZero)
        self.buttonAutoChop.setText("%s" %auto_chop_display)
        self.menuAutoChop = QtWidgets.QMenu()
        self.menuAutoChop.addAction("On", self.AutoChopAction1)
        self.menuAutoChop.addAction("Off", self.AutoChopAction2)
        self.buttonAutoChop.setMenu(self.menuAutoChop)
        self.buttonPowCal.setText("Factory")
        self.menuPowCal = QtWidgets.QMenu()
        self.menuPowCal.addAction("User", self.PowCalAction1)
        self.menuPowCal.addAction("Factory", self.PowCalAction2)
        self.buttonPowCal.setMenu(self.menuPowCal)
        self.buttonAmpCorr.setText("%s" %amplitude_correction)
        self.menuAmpCorr = QtWidgets.QMenu()
        self.menuAmpCorr.addAction("1", self.AmpCorrAction1)
        self.menuAmpCorr.addAction("2", self.AmpCorrAction2)
        self.menuAmpCorr.addAction("3", self.AmpCorrAction3)
        self.menuAmpCorr.addAction("4", self.AmpCorrAction4)
        if amplitude_correction_mode == '1':
            amplitude_correction_mode = 'On'
        elif amplitude_correction_mode == '0':
            amplitude_correction_mode = 'Off'    
        self.buttonAmpCorr.setMenu(self.menuAmpCorr)
        self.buttonAmpCorrMode.setText("%s" %amplitude_correction_mode)
        self.menuAmpCorrMode = QtWidgets.QMenu()
        self.menuAmpCorrMode.addAction("On", self.AmpCorrModeAction1)
        self.menuAmpCorrMode.addAction("Off", self.AmpCorrModeAction2)
        self.buttonAmpCorrMode.setMenu(self.menuAmpCorrMode)

        # Populate text fields
        self.labelUserPowCal.setText(str(instrument1.query("CALibration:POWer:DATE?")).rstrip())
        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def AmpUnitsAction1(self):
        self.buttonAmpUnits.setText("Auto")

    def AmpUnitsAction2(self):
        self.buttonAmpUnits.setText("W")

    def AutoRangAction1(self):
        self.buttonAutoRang.setText("On")

    def AutoRangAction2(self):
        self.buttonAutoRang.setText("Off")

    def AutoZeroAction1(self):
        self.buttonAutoZero.setText("On")

    def AutoZeroAction2(self):
        self.buttonAutoZero.setText("Off")

    def AutoChopAction1(self):
        self.buttonAutoChop.setText("On")

    def AutoChopAction2(self):
        self.buttonAutoChop.setText("Off")

    def PowCalAction1(self):
        self.buttonPowCal.setText("User")

    def PowCalAction2(self):
        self.buttonPowCal.setText("Factory")

    def AmpCorrAction1(self):
        self.buttonAmpCorr.setText("1")

    def AmpCorrAction2(self):
        self.buttonAmpCorr.setText("2")

    def AmpCorrAction3(self):
        self.buttonAmpCorr.setText("3")

    def AmpCorrAction4(self):
        self.buttonAmpCorr.setText("4")

    def AmpCorrModeAction1(self):
        self.buttonAmpCorrMode.setText("On")

    def AmpCorrModeAction2(self):
        self.buttonAmpCorrMode.setText("Off")

    def onAccept(self):
        global logLin
        global amplitude_units
        global auto_ranging
        global auto_range_display
        global auto_zero
        global auto_zero_display
        global auto_chop
        global auto_chop_display
        global amplitude_correction
        global amplitude_correction_mode
        
        if self.buttonAmpUnits.text() == "Auto":
            amplitude_units = 'dB'
        else:
            amplitude_units = 'W'

        if self.buttonAutoRang.text() == "On":
            instrument1.write("SENSe:POWer:DC:RANGe:AUTO ON")
            auto_ranging = '1'
            auto_range_display = 'On'
        else:
            instrument1.write("SENSe:POWer:DC:RANGe:AUTO OFF")
            auto_ranging = '0'
            auto_range_display = 'Off'

        if self.buttonAutoZero.text() == 'On':
            instrument1.write("CALibration:ZERO:AUTO 1")
            auto_zero = '1'
            auto_zero_display = 'On'
        else:
            instrument1.write("CALibration:ZERO:AUTO 0")
            auto_zero = '0'
            auto_zero_display = 'Off'

        if self.buttonAutoChop.text() == 'On':
            instrument1.write("SENSe:CHOP:STATe 1")
            auto_chop = '1'
            auto_chop_display = 'On'
        else:
            instrument1.write("SENSe:CHOP:STATe 0")
            auto_chop = '0'
            auto_chop_display = 'Off'

        amplitude_correction = str(self.buttonAmpCorr.text())
        instrument1.write("SENSe:CORRection:CSET %s" %amplitude_correction)

        amplitude_correction_mode = str(self.buttonAmpCorrMode.text())
        instrument1.write("SENSe:CORRection:STATe %s" %amplitude_correction_mode)
        return 
        
    def onReject(self):
        return

# Window to change wavelength setup paramters (global)
class WavelengthSetup(QtWidgets.QDialog, Ui_wavelengthSetupWindow):
    def __init__(self, parent=None):
        super(WavelengthSetup, self).__init__(parent)
        self.setupUi(self)
        wavelengthOffset = str(ast.literal_eval(instrument1.query("SENSe:WAVelength:OFFSet?")))
        wavelengthStepSize = str(ast.literal_eval(instrument1.query("SENse:WAVelength:CENTer:STEP:INCRement?")))
        wavelengthOffset = str(conversions.str2float(wavelengthOffset, '%s' %wavelength_units))
        wavelengthStepSize = str(conversions.str2float(wavelengthStepSize, '%s' %wavelength_units))
        self.buttonWLUnits.setText("%s" %wavelength_units)
        self.menuWLUnits = QtWidgets.QMenu()
        self.menuWLUnits.addAction("nm", self.WLUnitsAction1)
        self.menuWLUnits.addAction("um", self.WLUnitsAction2)
        self.menuWLUnits.addAction("Ang", self.WLUnitsAction3)
        self.buttonWLUnits.setMenu(self.menuWLUnits)
        self.lineWLOffset.setText("%s" %wavelengthOffset)
        self.label_3.setText("%s" %wavelength_units)
        self.label_5.setText("%s" %wavelength_units)
        self.lineWLStep.setText("%s" %wavelengthStepSize)
        self.buttonWLRef.setText("%s" %wavelengthRefIn)
        self.menuWLRef = QtWidgets.QMenu()
        self.menuWLRef.addAction("AIR", self.WLRefAction1)
        self.menuWLRef.addAction("VAC", self.WLRefAction2)
        self.buttonWLRef.setMenu(self.menuWLRef)

        # Prevent user input of non doubles
        validator = QtGui.QDoubleValidator()
        self.lineWLOffset.setValidator(validator)
        self.lineWLStep.setValidator(validator)

        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def WLUnitsAction1(self):
        global wavelength_units
        self.buttonWLUnits.setText("nm")
        wavelength_units = "nm"
        wavelength_units_display = 'm'

    def WLUnitsAction2(self):
        global wavelength_units
        self.buttonWLUnits.setText("um")
        wavelength_units = "um"
        wavelength_units_display = 'm'

    def WLUnitsAction3(self):
        global wavelength_units
        self.buttonWLUnits.setText("Ang")
        wavelength_units = "Ang"
        wavelength_units_display = 'Ang'

    def WLRefAction1(self):
        self.buttonWLRef.setText("AIR")

    def WLRefAction2(self):
        self.buttonWLRef.setText("VAC")

    def onAccept(self):
        global wavelengthRefIn
        
        if self.buttonWLUnits.text() == "nm":
            wavelength_units = "nm"
            wavelength_units_display = 'm'
        elif self.buttonWLUnits.text() == "um":
            wavelength_units = "um"
            wavelength_units_display = 'm'
        else:
            wavelength_units = "Ang"
            wavelength_units_display = 'Ang'

        wavelengthOffset = str(self.lineWLOffset.text())
        wavelengthStepSize = str(self.lineWLStep.text())
        wavOff = "SENSe:WAVelength:OFFSet " + "%s%s" %(wavelengthOffset,wavelength_units)
        wavStep = "SENse:WAVelength:CENTer:STEP:INCRement " + "%s%s" %(wavelengthStepSize,wavelength_units)
        instrument1.write(wavOff)
        instrument1.write(wavStep)
        
        if self.buttonWLRef.text() == "AIR":
            instrument1.write("SENSe:CORRection:RVELocity:MEDium AIR")
            wavelengthRefIn = "AIR"
        else:
            instrument1.write("SENSe:CORRection:RVELocity:MEDium VAC")
            wavelengthRefIn = "VAC"
        return

    def onReject(self):
        return

# Window to change marker setup parameters (global)
class MarkerSetup(QtWidgets.QDialog, Ui_markerSetupWindow):
    def __init__(self, MkrNo, parent=None):
        super(MarkerSetup, self).__init__(parent)
        global mkr_units
        global BW_units
        global delta_units
        global mkrInterpOnOff
        global BWInterpOnOff
        global mkrThreshOnOff
        global noiseMkrBW
        global OSNRType
        global OSNROffset
        global peakExcur
        global pitExcur
        global userMkrThresh
        global active_marker
        global validator
        
        
        self.setupUi(self)
        self.buttonNormMkrUnits.setText("%s" %mkr_units)
        self.menuNormMkrUnits = QtWidgets.QMenu()
        self.menuNormMkrUnits.addAction("nm", self.NormMkrUnitsAction1)
        self.menuNormMkrUnits.addAction("um", self.NormMkrUnitsAction2)
        self.menuNormMkrUnits.addAction("Ang", self.NormMkrUnitsAction3)
        self.menuNormMkrUnits.addAction("GHz", self.NormMkrUnitsAction4)
        self.menuNormMkrUnits.addAction("THz", self.NormMkrUnitsAction5)
        self.buttonNormMkrUnits.setMenu(self.menuNormMkrUnits)
        self.buttonBWMkrUnits.setText("%s" %BW_units)
        self.menuBWMkrUnits = QtWidgets.QMenu()
        self.menuBWMkrUnits.addAction("nm", self.BWMkrUnitsAction1)
        self.menuBWMkrUnits.addAction("um", self.BWMkrUnitsAction2)
        self.menuBWMkrUnits.addAction("Ang", self.BWMkrUnitsAction3)
        self.menuBWMkrUnits.addAction("GHz", self.BWMkrUnitsAction4)
        self.menuBWMkrUnits.addAction("THz", self.BWMkrUnitsAction5)
        self.buttonBWMkrUnits.setMenu(self.menuBWMkrUnits)
        self.buttonDeltaMkrUnits.setText("%s" %delta_units)
        self.menuDeltaMkrUnits = QtWidgets.QMenu()
        self.menuDeltaMkrUnits.addAction("nm", self.DeltaMkrUnitsAction1)
        self.menuDeltaMkrUnits.addAction("um", self.DeltaMkrUnitsAction2)
        self.menuDeltaMkrUnits.addAction("Ang", self.DeltaMkrUnitsAction3)
        self.menuDeltaMkrUnits.addAction("GHz", self.DeltaMkrUnitsAction4)
        self.menuDeltaMkrUnits.addAction("THz", self.DeltaMkrUnitsAction5)
        self.buttonDeltaMkrUnits.setMenu(self.menuDeltaMkrUnits)
        self.buttonMkrInterp.setText("%s" %mkrInterpOnOff)
        self.menuMkrInterp = QtWidgets.QMenu()
        self.menuMkrInterp.addAction("ON", self.MkrInterpAction1)
        self.menuMkrInterp.addAction("OFF", self.MkrInterpAction2)
        self.buttonMkrInterp.setMenu(self.menuMkrInterp)
        self.buttonBWMkrInterp.setText("%s" %BWInterpOnOff)
        self.menuBWMkrInterp = QtWidgets.QMenu()
        self.menuBWMkrInterp.addAction("ON", self.BWMkrInterpAction1)
        self.menuBWMkrInterp.addAction("OFF", self.BWMkrInterpAction2)
        self.buttonBWMkrInterp.setMenu(self.menuBWMkrInterp)
        self.buttonUserMkrThresh.setText("%s" %mkrThreshOnOff)
        self.menuUserMkrThresh = QtWidgets.QMenu()
        self.menuUserMkrThresh.addAction("ON", self.UserMkrThreshAction1)
        self.menuUserMkrThresh.addAction("OFF", self.UserMkrThreshAction2)
        self.buttonUserMkrThresh.setMenu(self.menuUserMkrThresh)
        self.buttonNoiseMkrBW.setText("%s nm" %noiseMkrBW)
        self.menuNoiseMkrBW = QtWidgets.QMenu()
        self.menuNoiseMkrBW.addAction("0.1 nm", self.NoiseMkrBWAction1)
        self.menuNoiseMkrBW.addAction("1.0 nm", self.NoiseMkrBWAction2)
        self.buttonNoiseMkrBW.setMenu(self.menuNoiseMkrBW)
        self.buttonOSNR.setText("%s" %OSNRType)
        self.menuOSNR = QtWidgets.QMenu()
        self.menuOSNR.addAction("PIT", self.OSNRAction1)
        self.menuOSNR.addAction("Auto", self.OSNRAction2)
        self.menuOSNR.addAction("Manual", self.OSNRAction3)
        self.buttonOSNR.setMenu(self.menuOSNR)
        peakExcur = str(conversions.str2float(peakExcur,'dB'))
        self.linePeakExcur.setText("%s" %peakExcur)
        pitExcur = str(conversions.str2float(pitExcur,'dB'))
        self.linePitExcur.setText("%s" %pitExcur)
        validator = QtGui.QDoubleValidator()
        if OSNRType == 'MAN':
            self.lineOSNR.setText("%s" %OSNROffset)
            self.lineOSNR.setValidator(validator)
        else:
            self.lineOSNR.setText("DISABLED")
        if mkrThreshOnOff == 'ON':
            self.lineSrchThresh.setText("%s" %userMkrThresh)
            self.lineSrchThresh.setValidator(validator)
        else:
            self.lineSrchThresh.setText("DISABLED")

        # Prevent user input of non doubles
        validator = QtGui.QDoubleValidator()
        self.linePeakExcur.setValidator(validator)
        self.linePitExcur.setValidator(validator)

        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def NormMkrUnitsAction1(self):
        self.buttonNormMkrUnits.setText("nm")

    def NormMkrUnitsAction2(self):
        self.buttonNormMkrUnits.setText("um")

    def NormMkrUnitsAction3(self):
        self.buttonNormMkrUnits.setText("Ang")

    def NormMkrUnitsAction4(self):
        self.buttonNormMkrUnits.setText("GHz")

    def NormMkrUnitsAction5(self):
        self.buttonNormMkrUnits.setText("THz")

    def BWMkrUnitsAction1(self):
        self.buttonBWMkrUnits.setText("nm")

    def BWMkrUnitsAction2(self):
        self.buttonBWMkrUnits.setText("um")

    def BWMkrUnitsAction3(self):
        self.buttonBWMkrUnits.setText("Ang")

    def BWMkrUnitsAction4(self):
        self.buttonBWMkrUnits.setText("GHz")

    def BWMkrUnitsAction5(self):
        self.buttonBWMkrUnits.setText("THz")

    def DeltaMkrUnitsAction1(self):
        self.buttonDeltaMkrUnits.setText("nm")

    def DeltaMkrUnitsAction2(self):
        self.buttonDeltaMkrUnits.setText("um")

    def DeltaMkrUnitsAction3(self):
        self.buttonDeltaMkrUnits.setText("Ang")

    def DeltaMkrUnitsAction4(self):
        self.buttonDeltaMkrUnits.setText("GHz")

    def DeltaMkrUnitsAction5(self):
        self.buttonDeltaMkrUnits.setText("THz")

    def MkrInterpAction1(self):
        self.buttonMkrInterp.setText("ON")

    def MkrInterpAction2(self):
        self.buttonMkrInterp.setText("OFF")

    def BWMkrInterpAction1(self):
        self.buttonBWMkrInterp.setText("ON")

    def BWMkrInterpAction2(self):
        self.buttonBWMkrInterp.setText("OFF")

    def UserMkrThreshAction1(self):
        self.buttonUserMkrThresh.setText("ON")
        self.lineSrchThresh.setText("%s" %userMkrThresh)
        self.lineSrchThresh.setValidator(validator)

    def UserMkrThreshAction2(self):
        self.buttonUserMkrThresh.setText("OFF")
        self.lineSrchThresh.setText("DISABLED")

    def NoiseMkrBWAction1(self):
        self.buttonNoiseMkrBW.setText("0.1 nm")

    def NoiseMkrBWAction2(self):
        self.buttonNoiseMkrBW.setText("1.0 nm")

    def OSNRAction1(self):
        self.buttonOSNR.setText("PIT")
        self.lineOSNR.setText("DISABLED")

    def OSNRAction2(self):
        self.buttonOSNR.setText("AUTO")
        self.lineOSNR.setText("DISABLED")

    def OSNRAction3(self):
        self.buttonOSNR.setText("MAN")
        self.lineOSNR.setText("%s" %OSNROffset)
        self.lineOSNR.setValidator(validator)

    def onAccept(self):
        global mkr_units
        global BW_units
        global delta_units
        global mkrInterpOnOff
        global BWInterpOnOff
        global mkrThreshOnOff
        global noiseMkrBW
        global OSNRType
        global OSNROffset
        global peakExcur
        global pitExcur
        global userMkrThresh
        global active_marker
        
        mkr_units = self.buttonNormMkrUnits.text()
        delta_units = self.buttonDeltaMkrUnits.text()
        BW_units = self.buttonBWMkrUnits.text()

        if self.buttonMkrInterp.text() == "ON":
            mkrInterpOnOff = 'ON'
            instrument1.write("CALCulate:MARKer%s:INT 1" %active_marker)
        else:
            mkrInterpOnOff = 'OFF'
            instrument1.write("CALCulate:MARKer%s:INT 0" %active_marker)

        if self.buttonBWMkrInterp.text() == "ON":
            BWInterpOnOff = 'ON'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:INT 1" %active_marker)
        else:
            BWInterpOnOff = 'OFF'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:INT 0" %active_marker)

        peakExcur = str(self.linePeakExcur.text()).rstrip()
        instrument1.write("CALCulate:MARKer%s:PEXCursion:PEAK %sdB" %(active_marker,peakExcur))

        pitExcur = str(self.linePitExcur.text()).rstrip()
        instrument1.write("CALCulate:MARKer%s:PEXCursion:PIT %sdB" %(active_marker,pitExcur))

        if self.buttonUserMkrThresh.text() == "ON":
            mkrThreshOnOff = 'ON'
            instrument1.write("CALCulate:THReshold:STATe 1")
            userMkrThresh = str(self.lineSrchThresh.text()).rstrip()
            instrument1.write("CALCulate:THReshold %sdBm" %userMkrThresh)
        else:
            mkrThreshOnOff = 'OFF'
            instrument1.write("CALCulate:THReshold:STATe 0")

        if self.buttonNoiseMkrBW.text() == "0.1 nm":
            noiseMkrBW = '0.1'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:BANDwidth 0.1nm" %active_marker)
        else:
            noiseMkrBW = '1.0'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:NOISe:BANDwidth 1nm" %active_marker)

        if self.buttonOSNR.text() == "MAN":
            OSNRType = 'MAN'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:MODE %s" %(active_marker, OSNRType))
            OSNROffset = str(self.lineOSNR.text()).rstrip()
            instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:OFFSet %snm" %(active_marker, OSNROffset))
        elif self.buttonOSNR.text() == "AUTO":
            OSNRType = 'AUTO'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:MODE %s" %(active_marker, OSNRType))
        else:
            OSNRType = 'PIT'
            instrument1.write("CALCulate:MARKer%s:FUNCtion:OSNR:MODE %s" %(active_marker, OSNRType))
        return

    def onReject(self):
        return

# Window to change advanced line marker parameters (global)
class AdvancedLineMarkerWindow(QtWidgets.QDialog, Ui_advancedLineMarkerWindow):
    def __init__(self, parent=None):
        super(AdvancedLineMarkerWindow, self).__init__(parent)
        global search_limit
        global sweep_limit
        global integral_limit
        global trace_integral
        
        self.setupUi(self)
        self.buttonSweepLimit.setText("%s" %sweep_limit)
        self.menuSweepLimit = QtWidgets.QMenu()
        self.menuSweepLimit.addAction("On", self.SweepLimitAction1)
        self.menuSweepLimit.addAction("Off", self.SweepLimitAction2)
        self.buttonSweepLimit.setMenu(self.menuSweepLimit)
        self.buttonSrchLimit.setText("%s" %search_limit)
        self.menuSrchLimit = QtWidgets.QMenu()
        self.menuSrchLimit.addAction("On", self.SrchLimitAction1)
        self.menuSrchLimit.addAction("Off", self.SrchLimitAction2)
        self.buttonSrchLimit.setMenu(self.menuSrchLimit)
        self.buttonIntegLimit.setText("%s" %integral_limit)
        self.menuIntegLimit = QtWidgets.QMenu()
        self.menuIntegLimit.addAction("On", self.IntegLimitAction1)
        self.menuIntegLimit.addAction("Off", self.IntegLimitAction2)
        self.buttonIntegLimit.setMenu(self.menuIntegLimit)
        self.buttonTraceInteg.setText("%s" %trace_integral)
        self.menuTraceInteg = QtWidgets.QMenu()
        self.menuTraceInteg.addAction("On", self.TraceIntegAction1)
        self.menuTraceInteg.addAction("Off", self.TraceIntegAction2)
        self.buttonTraceInteg.setMenu(self.menuTraceInteg)

        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def SweepLimitAction1(self):
        self.buttonSweepLimit.setText("On")

    def SweepLimitAction2(self):
        self.buttonSweepLimit.setText("Off")

    def SrchLimitAction1(self):
        self.buttonSrchLimit.setText("On")

    def SrchLimitAction2(self):
        self.buttonSrchLimit.setText("Off")

    def IntegLimitAction1(self):
        self.buttonIntegLimit.setText("On")

    def IntegLimitAction2(self):
        self.buttonIntegLimit.setText("Off")

    def TraceIntegAction1(self):
        self.buttonTraceInteg.setText("On")

    def TraceIntegAction2(self):
        self.buttonTraceInteg.setText("Off")

    def onAccept(self):
        global search_limit
        global sweep_limit
        global integral_limit
        global trace_integral
        global lineMarkerOnOff
        
        if self.buttonSweepLimit.text() == 'On':
            instrument1.write("SENSe:WAVelength:SRANge:STATe ON")
            self.buttonSweepLimit.setText("On")
            sweep_limit = 'On'
            sweep_flag = '1'
        elif self.buttonSweepLimit.text() == 'Off':
            instrument1.write("SENSe:WAVelength:SRANge:STATe OFF")
            self.buttonSweepLimit.setText("Off")
            sweep_limit = 'Off'
            sweep_flag = '0'

        if self.buttonSrchLimit.text() == 'On':
            instrument1.write("CALCulate:MARKer:SRANge:STATe ON")
            self.buttonSrchLimit.setText("On")
            search_limit = 'On'
            search_flag = '1'
        elif self.buttonSrchLimit.text() == 'Off':
            instrument1.write("CALCulate:MARKer:SRANge:STATe OFF")
            self.buttonSrchLimit.setText("Off")
            search_limit = 'Off'
            search_flag = '0'

        if self.buttonIntegLimit.text() == 'On':
            instrument1.write("CALCulate:TPOWer:IRANge:STATe ON")
            self.buttonIntegLimit.setText("On")
            integral_limit = 'On'
        elif self.buttonIntegLimit.text() == 'Off':
            instrument1.write("CALCulate:TPOWer:IRANge:STATe OFF")
            self.buttonIntegLimit.setText("Off")
            integral_limit = 'Off'

        if self.buttonTraceInteg.text() == 'On':
            instrument1.write("CALCulate:TPOWer:STATe ON")
            self.buttonTraceInteg.setText("On")
            trace_integral = 'On'
            self.infoDisplay()
        elif self.buttonTraceInteg.text() == 'Off':
            instrument1.write("CALCulate:TPOWer:STATe OFF")
            self.buttonTraceInteg.setText("Off")
            trace_integral = 'Off'
            self.infoDisplay()

        if sweep_limit == 'On' or search_limit == 'On' or integral_limit == 'On' or trace_integral == 'On':
            lineMarkerOnOff = 'On'
        else:
            lineMarkerOnOff = 'Off'
        return

    def onReject(self):
        return

# Window to change system parameters (global)
class SystemWindow(QtWidgets.QDialog, Ui_systemWindow):
    def __init__(self, parent=None):
        super(SystemWindow, self).__init__(parent)
        self.setupUi(self)
        self.buttonSigSource.setText("External")
        self.menuSigSource = QtWidgets.QMenu()
        self.menuSigSource.addAction("External", self.SigSourceAction1)
        self.menuSigSource.addAction("Calibrator", self.SigSourceAction2)
        self.buttonSigSource.setMenu(self.menuSigSource)
        self.buttonWLRef.setText("%s" %wavelengthRefIn)
        self.menuWLRef = QtWidgets.QMenu()
        self.menuWLRef.addAction("AIR", self.WLRefAction1)
        self.menuWLRef.addAction("VAC", self.WLRefAction2)
        self.buttonWLRef.setMenu(self.menuWLRef)

        # Populate text fields
        self.labelFacPowCal.setText(str(instrument1.query("CALibration:DATE?")).rstrip())
        self.labelUserPowCal.setText(str(instrument1.query("CALibration:POWer:DATE?")).rstrip())
        self.lineCalPower.setText("%s" %Power_Calibration)
        self.lineCalWL.setText("%s" %Power_Calibration)

        self.lineIncrement.setText("%s" %indent_margin)
        
        self.labelFacWLCal.setText(str(instrument1.query("CALibration:DATE?")).rstrip()) 
        self.labelUserWLCal.setText(str(instrument1.query("CALibration:WAVelength:DATE?")).rstrip())

        self.firmwareLabel.setText(str(instrument1.query("*IDN?")).rstrip())

        # Prevent user input of non doubles
        validator = QtGui.QDoubleValidator()
        self.lineCalWL.setValidator(validator)
        self.lineCalPower.setValidator(validator)  
        self.lineSetCalWL.setValidator(validator) 

        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)   

    def SigSourceAction1(self):
        self.buttonSigSource.setText("External")

    def SigSourceAction2(self):
        self.buttonSigSource.setText("Calibrator")

    def WLRefAction1(self):
        self.buttonWLRef.setText("AIR")

    def WLRefAction2(self):
        self.buttonWLRef.setText("VAC")

    def onAccept(self):
        global wavelengthRefIn
        global indent_margin

        if self.buttonWLRef.text() == "AIR":
            instrument1.write("SENSe:CORRection:RVELocity:MEDium AIR")
            wavelengthRefIn = "AIR"
            self.buttonWLRef.setText("AIR")
        else:
            instrument1.write("SENSe:CORRection:RVELocity:MEDium VAC")
            wavelengthRefIn = "VAC"
            self.buttonWLRef.setText("VAC")
        indent_margin = int(self.lineIncrement.text())
        return

    def onReject(self):
        return

# Window to allow the user to place a marker on a trace in the graph
class NewMarkerWindow(QtWidgets.QDialog, Ui_newMarkerWindow):
    def __init__(self, active_marker, active_trace, trace_a_param, trace_b_param, trace_c_param, trace_d_param, trace_e_param, trace_f_param, parent=None):
        super(NewMarkerWindow, self).__init__(parent)
        self.setupUi(self)
        self.buttonMkrSel.setText("Mkr %s" %active_marker)
        self.menuMkrSel = QtWidgets.QMenu()
        self.menuMkrSel.addAction("Mkr 1", self.MkrSelAction1)
        self.menuMkrSel.addAction("Mkr 2", self.MkrSelAction2)
        self.menuMkrSel.addAction("Mkr 3", self.MkrSelAction3)
        self.menuMkrSel.addAction("Mkr 4", self.MkrSelAction4)
        self.buttonMkrSel.setMenu(self.menuMkrSel)
        self.buttonTrcSel.setText("Trace %s" %active_trace[2])
        self.menuTrcSel = QtWidgets.QMenu()
        if trace_a_param[1] == 'ON':
            self.menuTrcSel.addAction("Trace A", self.TrcSelAction1)
        if trace_b_param[1] == 'ON':
            self.menuTrcSel.addAction("Trace B", self.TrcSelAction2)
        if trace_c_param[1] == 'ON':
            self.menuTrcSel.addAction("Trace C", self.TrcSelAction3)
        if trace_d_param[1] == 'ON':
            self.menuTrcSel.addAction("Trace D", self.TrcSelAction4)
        if trace_e_param[1] == 'ON':
            self.menuTrcSel.addAction("Trace E", self.TrcSelAction5)
        if trace_f_param[1] == 'ON':
            self.menuTrcSel.addAction("Trace F", self.TrcSelAction6)
        self.buttonTrcSel.setMenu(self.menuTrcSel)

        self.accepted.connect(self.onAccept)
        self.rejected.connect(self.onReject)

    def MkrSelAction1(self):
        self.buttonMkrSel.setText("Mkr 1")

    def MkrSelAction2(self):
        self.buttonMkrSel.setText("Mkr 2")

    def MkrSelAction3(self):
        self.buttonMkrSel.setText("Mkr 3")

    def MkrSelAction4(self):
        self.buttonMkrSel.setText("Mkr 4")

    def TrcSelAction1(self):
        self.buttonTrcSel.setText("Trace A")

    def TrcSelAction2(self):
        self.buttonTrcSel.setText("Trace B")

    def TrcSelAction3(self):
        self.buttonTrcSel.setText("Trace C")

    def TrcSelAction4(self):
        self.buttonTrcSel.setText("Trace D")

    def TrcSelAction5(self):
        self.buttonTrcSel.setText("Trace E")

    def TrcSelAction6(self):
        self.buttonTrcSel.setText("Trace F")

    def onAccept(self):
        self.marker = self.buttonMkrSel.text()
        self.trace = self.buttonTrcSel.text()
        self.selection = 1
        return self.marker, self.trace, self.selection

    def onReject(self):
        self.selection = 0
        return self.selection


# Background class for Agilent 86142B to run continuous sweeps when enabled
class Thread(QtCore.QThread):
    sig = QtCore.pyqtSignal()
    sig2 = QtCore.pyqtSignal()
    sig3 = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)

    def __del__(self):
        self.wait()
        
    def run(self):
        global contOnOff
        global inUse
        global plotDone
        global reset
        global menuBlock
        plotDone = 0
        while contOnOff == 1:
            if inUse == 0:
                plotDone = 0
                if reset == 1:
                    time.sleep(1)
                self.contTrace()
                self.contMarkers()
                self.sig.emit()
                self.sleep(0.2)
                plotDone = 1
            
        if contOnOff == 0:
            self.sig2.emit()
               
    def contTrace(self):
        global traceA
        global traceB
        global traceC
        global traceD
        global traceE
        global traceF
        global trace_x_values
        global trace_y_values
        global ref_level
        global x_ref
        global y_ref
        global trace_a_param
        global trace_b_param
        global trace_c_param
        global trace_d_param
        global trace_e_param
        global trace_f_param
        global frame_start
        global frame_stop

        if trace_a_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRA")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRA")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRA")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceA = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
                
        if trace_b_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRB")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRB")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRB")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceB = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly

        if trace_c_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRC")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRc")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRC")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceC = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            
        if trace_d_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRD")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRD")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRD")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceD = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            
        if trace_e_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRE")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRE")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRE")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceE = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly
            
        if trace_f_param[1] == "ON":
            trace_start = ast.literal_eval(instrument1.query("TRACe:DATA:X:STARt? TRF")) # finds start of trace in right format
            trace_stop = ast.literal_eval(instrument1.query("TRACe:DATA:X:STOP? TRF")) # finds end of trace in right format
            trace_y_values = ast.literal_eval(instrument1.query("TRAC? TRF")) # obtains trace data for y values (power)
            trace_x_values = numpy.linspace(trace_start,trace_stop,len(trace_y_values)) # runs linspace function to create the equating x data points (wavelength)
            traceF = numpy.array([trace_x_values,trace_y_values]).T # combines the x and y trace data and formats it correctly

        frame_start = ast.literal_eval(instrument1.query("SENSe:WAVelength:STARt?")) # finds left hand side of display
        frame_stop = ast.literal_eval(instrument1.query("SENSe:WAVelength:STOP?")) # finds right hand side of display

        ref_level = instrument1.query("DISPlay:WINDow:TRACe:Y:SCALe:RLEVel?")
        ref_level = conversions.str2float(ref_level,"dBm")
        x_ref = numpy.linspace(frame_start,frame_stop,int(num_points))
        y_ref = numpy.ones(int(num_points))
        y_ref = ref_level*y_ref

    def mkr1Off(self):
        global mkr_1_param
        global mkr_1_extras
        if mkr_1_param[3] == 'ON':
            instrument1.write("CALCulate:MARKer1:FUNCtion:BANDwidth:STATe OFF")
            mkr_1_param[3] = 'OFF'
        if mkr_1_param[4] == 'ON':
            instrument1.write("CALCulate:MARKer1:FUNCtion:NOISe:STATe OFF")
            mkr_1_param[4] = 'OFF'
        if mkr_1_param[5] == 'ON':
            instrument1.write("CALCulate:MARKer1:FUNCtion:DELTa:STATe OFF")
            mkr_1_param[5] = 'OFF'
        if mkr_1_param[6] == 'ON':
            instrument1.write("CALCulate:MARKer1:FUNCtion:OSNR:STATe OFF")
            mkr_1_param[6] == 'OFF'
        mkr_1_extras = 0

    def mkr2Off(self):
        global mkr_2_param
        global mkr_2_extras
        if mkr_2_param[3] == 'ON':
            instrument1.write("CALCulate:MARKer2:FUNCtion:BANDwidth:STATe OFF")
            mkr_2_param[3] = 'OFF'
        if mkr_2_param[4] == 'ON':
            instrument1.write("CALCulate:MARKer2:FUNCtion:NOISe:STATe OFF")
            mkr_2_param[4] = 'OFF'
        if mkr_2_param[5] == 'ON':
            instrument1.write("CALCulate:MARKer2:FUNCtion:DELTa:STATe OFF")
            mkr_2_param[5] = 'OFF'
        if mkr_2_param[6] == 'ON':
            instrument1.write("CALCulate:MARKer2:FUNCtion:OSNR:STATe OFF")
            mkr_2_param[6] == 'OFF'
        mkr_2_extras = 0

    def mkr3Off(self):
        global mkr_3_param
        global mkr_3_extras
        if mkr_3_param[3] == 'ON':
            instrument1.write("CALCulate:MARKer3:FUNCtion:BANDwidth:STATe OFF")
            mkr_3_param[3] = 'OFF'
        if mkr_3_param[4] == 'ON':
            instrument1.write("CALCulate:MARKer3:FUNCtion:NOISe:STATe OFF")
            mkr_3_param[4] = 'OFF'
        if mkr_3_param[5] == 'ON':
            instrument1.write("CALCulate:MARKer3:FUNCtion:DELTa:STATe OFF")
            mkr_3_param[5] = 'OFF'
        if mkr_3_param[6] == 'ON':
            instrument1.write("CALCulate:MARKer3:FUNCtion:OSNR:STATe OFF")
            mkr_3_param[6] == 'OFF'
        mkr_3_extras = 0

    def mkr4Off(self):
        global mkr_4_param
        global mkr_4_extras
        if mkr_4_param[3] == 'ON':
            instrument1.write("CALCulate:MARKer4:FUNCtion:BANDwidth:STATe OFF")
            mkr_4_param[3] = 'OFF'
        if mkr_4_param[4] == 'ON':
            instrument1.write("CALCulate:MARKer4:FUNCtion:NOISe:STATe OFF")
            mkr_4_param[4] = 'OFF'
        if mkr_4_param[5] == 'ON':
            instrument1.write("CALCulate:MARKer4:FUNCtion:DELTa:STATe OFF")
            mkr_4_param[5] = 'OFF'
        if mkr_4_param[6] == 'ON':
            instrument1.write("CALCulate:MARKer4:FUNCtion:OSNR:STATe OFF")
            mkr_4_param[6] == 'OFF'
        mkr_4_extras = 0
            
    def contMarkers(self):
        global mkr_1_param
        global mkr_2_param
        global mkr_3_param
        global mkr_4_param
        global BW_1_param
        global BW_2_param
        global BW_3_param
        global BW_4_param
        global delta_1_param
        global delta_2_param
        global delta_3_param
        global delta_4_param
        global OSNR_1_param
        global OSNR_2_param
        global OSNR_3_param
        global OSNR_4_param
        global reset
        global mkr_1_index
        global mkr_2_index
        global mkr_3_index
        global mkr_4_index
        global mkr_1_extras
        global mkr_2_extras
        global mkr_3_extras
        global mkr_4_extras
        global integValue
        global resetGraph

        if lineMarkerOnOff == 'On' or traceIntOnOff == "ON":
            integValue = float(instrument1.query("CALCulate:TPOWer:DATA?"))
        
        if reset == 1:
            #####   MARKER 1    #####
            mkr_1_extras = 0
            if mkr_1_param[0] == "1":
                if mkr_1_param[3] == 'ON' or mkr_1_param[4] == 'ON' or mkr_1_param[5] == 'ON' or mkr_1_param[6] == 'ON':
                    mkr_1_extras = 1
                    self.mkr2Off()
                    self.mkr3Off()
                    self.mkr4Off()
                else:
                    markerXt = float(instrument1.query("CALCulate:MARKer1:X?"))
                    markerX = conversions.str2float(markerXt, mkr_units)
                    markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
                    mkr_1_param[1] = markerX
                    mkr_1_param[2] = markerY
                    i = 0
                    if mkr_1_param[7] == "TRA":
                        traceX = traceA[:,0]
                    elif mkr_1_param[7] == "TRB":
                        traceX = traceB[:,0]
                    elif mkr_1_param[7] == "TRC":
                        traceX = traceC[:,0]
                    elif mkr_1_param[7] == "TRD":
                        traceX = traceD[:,0]
                    elif mkr_1_param[7] == "TRE":
                        traceX = traceE[:,0]
                    elif mkr_1_param[7] == "TRF":
                        traceX = traceF[:,0]
                    error_thresh = 0.01
                    for i in range(len(traceX)):
                        distance_x = abs(traceX[i]-markerXt)
                        if distance_x < error_thresh:
                            mkr_1_index = i
                            error_thresh = distance_x

            #####    MARKER 2   #####
            mkr_2_extras = 0
            if mkr_2_param[0] == "1":
                if mkr_2_param[3] == 'ON' or mkr_2_param[4] == 'ON' or mkr_2_param[5] == 'ON' or mkr_2_param[6] == 'ON':
                    mkr_2_extras = 1
                    self.mkr1Off()
                    self.mkr3Off()
                    self.mkr4Off()
                else:
                    markerXt = float(instrument1.query("CALCulate:MARKer2:X?"))
                    markerX = conversions.str2float(markerXt, mkr_units)
                    markerY = float(instrument1.query("CALCulate:marker2:Y?"))
                    mkr_2_param[1] = markerX
                    mkr_2_param[2] = markerY
                    i = 0
                    if mkr_2_param[7] == "TRA":
                        traceX = traceA[:,0]
                    elif mkr_2_param[7] == "TRB":
                        traceX = traceB[:,0]
                    elif mkr_2_param[7] == "TRC":
                        traceX = traceC[:,0]
                    elif mkr_2_param[7] == "TRD":
                        traceX = traceD[:,0]
                    elif mkr_2_param[7] == "TRE":
                        traceX = traceE[:,0]
                    elif mkr_2_param[7] == "TRF":
                        traceX = traceF[:,0]
                    error_thresh = 0.01 
                    for i in range(len(traceX)):
                        distance_x = abs(traceX[i]-markerXt)
                        if distance_x < error_thresh:
                            mkr_2_index = i
                            error_thresh = distance_x
            
            #####   MARKER 3    #####
            mkr_3_extras = 0
            if mkr_3_param[0] == "1":
                if mkr_3_param[3] == 'ON' or mkr_3_param[4] == 'ON' or mkr_3_param[5] == 'ON' or mkr_3_param[6] == 'ON':
                    mkr_3_extras = 1
                    self.mkr1Off()
                    self.mkr2Off()
                    self.mkr4Off()
                else:
                    markerXt = float(instrument1.query("CALCulate:MARKer3:X?"))
                    markerX = conversions.str2float(markerXt, mkr_units)
                    markerY = float(instrument1.query("CALCulate:marker3:Y?"))
                    mkr_3_param[1] = markerX
                    mkr_3_param[2] = markerY
                    i = 0
                    if mkr_3_param[7] == "TRA":
                        traceX = traceA[:,0]
                    elif mkr_3_param[7] == "TRB":
                        traceX = traceB[:,0]
                    elif mkr_3_param[7] == "TRC":
                        traceX = traceC[:,0]
                    elif mkr_3_param[7] == "TRD":
                        traceX = traceD[:,0]
                    elif mkr_3_param[7] == "TRE":
                        traceX = traceE[:,0]
                    elif mkr_3_param[7] == "TRF":
                        traceX = traceF[:,0]
                    error_thresh = 0.01 
                    for i in range(len(traceX)):
                        distance_x = abs(traceX[i]-markerXt)
                        if distance_x < error_thresh:
                            mkr_3_index = i
                            error_thresh = distance_x
            
            #####   MARKER 4    #####
            mkr_4_extras = 0
            if mkr_4_param[0] == "1":
                if mkr_4_param[3] == 'ON' or mkr_4_param[4] == 'ON' or mkr_4_param[5] == 'ON' or mkr_4_param[6] == 'ON':
                    mkr_4_extras = 1
                    self.mkr1Off()
                    self.mkr2Off()
                    self.mkr3Off()
                else:
                    markerXt = float(instrument1.query("CALCulate:MARKer4:X?"))
                    markerX = conversions.str2float(markerXt, mkr_units)
                    markerY = float(instrument1.query("CALCulate:marker4:Y?"))
                    mkr_4_param[1] = markerX
                    mkr_4_param[2] = markerY
                    i = 0
                    if mkr_4_param[7] == "TRA":
                        traceX = traceA[:,0]
                    elif mkr_4_param[7] == "TRB":
                        traceX = traceB[:,0]
                    elif mkr_4_param[7] == "TRC":
                        traceX = traceC[:,0]
                    elif mkr_4_param[7] == "TRD":
                        traceX = traceD[:,0]
                    elif mkr_4_param[7] == "TRE":
                        traceX = traceE[:,0]
                    elif mkr_4_param[7] == "TRF":
                        traceX = traceF[:,0]
                    error_thresh = 0.01 
                    for i in range(len(traceX)):
                        distance_x = abs(traceX[i]-markerXt)
                        if distance_x < error_thresh:
                            mkr_4_index = i
                            error_thresh = distance_x
            reset = 0
            resetGraph = 1
            self.sig3.emit()
        else:
            if mkr_1_param[0] == "1":
                if mkr_1_extras == 1:
                    if mkr_1_param[3] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer1:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
                        mkr_1_param[1] = markerX
                        mkr_1_param[2] = markerY
                        trc = mkr_1_param[7]
                        xL = str(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:LEFT?").rstrip())
                        BWxL = conversions.str2float(xL, BW_units)
                        xR = str(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
                        BWxR = conversions.str2float(xR, BW_units)
                        xC = str(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:CENTer?").rstrip())
                        BWxC = conversions.str2float(xC, BW_units)
                        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer1:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
                        BWyL = mkr_1_param[2] + mkrBWY
                        BWyR = mkr_1_param[2] + mkrBWY
                        BW_1_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                    elif mkr_1_param[4] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer1:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
                        mkr_1_param[1] = markerX
                        mkr_1_param[2] = markerY
                    # Delta
                    elif mkr_1_param[5] == "ON":
                        delta_distance = instrument1.query("CALC:MARK1:FUNC:DELTa:X:OFFset?")
                        delta_distance = conversions.str2float(delta_distance,delta_units)
                        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:X?").rstrip()),delta_units)
                        markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
                        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNC:DELta:X:REF?").rstrip()),delta_units)
                        markerYRef = float(instrument1.query("CALCulate:MARKer1:FUNC:DELta:Y:REF?"))
                        delta_1_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                    # OSNR
                    elif mkr_1_param[6] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer1:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer1:Y?"))
                        mkr_1_param[1] = markerX
                        mkr_1_param[2] = markerY
                        OSNRVal = float(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:RESult?"))
                        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
                        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
                        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
                        if mkr_1_param[7] == 'TRA':
                            trace_data = traceA
                        elif mkr_1_param[7] == 'TRB':
                            trace_data = traceB
                        elif mkr_1_param[7] == 'TRC':
                            trace_data = traceC
                        elif mkr_1_param[7] == 'TRD':
                            trace_data = traceD
                        elif mkr_1_param[7] == 'TRE':
                            trace_data = traceE
                        elif mkr_1_param[7] == 'TRF':
                            trace_data = traceF
                        trace_x = trace_data[:,0]
                        trace_y = trace_data[:,1]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyL = trace_y[mkr_index]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyR = trace_y[mkr_index]
                        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
                        OSNRyC = float(instrument1.query("CALCulate:MARKer1:FUNCtion:OSNR:Y:CENTer?"))
                        
                        if abs(OSNRyC) > 100:
                            OSNRyC = 0
                            OSNRVal = 0
                        OSNR_1_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                    
                else:
                    if mkr_1_param[7] == "TRA":
                        traceX = traceA[:,0]
                        traceY = traceA[:,1]
                    elif mkr_1_param[7] == "TRB":
                        traceX = traceB[:,0]
                        traceY = traceB[:,1]
                    elif mkr_1_param[7] == "TRC":
                        traceX = traceC[:,0]
                        traceY = traceC[:,1]
                    elif mkr_1_param[7] == "TRD":
                        traceX = traceD[:,0]
                        traceY = traceD[:,1]
                    elif mkr_1_param[7] == "TRE":
                        traceX = traceE[:,0]
                        traceY = traceE[:,1]
                    elif mkr_1_param[7] == "TRF":
                        traceX = traceF[:,0]
                        traceY = traceF[:,1]
                    markerX = traceX[mkr_1_index]
                    markerY = traceY[mkr_1_index]
                    mkr_1_param[1] = conversions.str2float(markerX,mkr_units)
                    mkr_1_param[2] = markerY

            if mkr_2_param[0] == "1":
                if mkr_2_extras == 1:
                    # Bandwidth
                    if mkr_2_param[3] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer2:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer2:Y?"))
                        mkr_2_param[1] = markerX
                        mkr_2_param[2] = markerY
                        trc = mkr_2_param[7]
                        xL = str(instrument1.query("CALCulate:marker2:FUNCtion:BANDwidth:X:LEFT?").rstrip())
                        BWxL = conversions.str2float(xL, BW_units)
                        xR = str(instrument1.query("CALCulate:marker2:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
                        BWxR = conversions.str2float(xR, BW_units)
                        xC = str(instrument1.query("CALCulate:marker2:FUNCtion:BANDwidth:X:CENTer?").rstrip())
                        BWxC = conversions.str2float(xC, BW_units)
                        mkrBWY = conversions.str2float(instrument1.query("CALCulate:marker2:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
                        BWyL = mkr_2_param[2] + mkrBWY
                        BWyR = mkr_2_param[2] + mkrBWY
                        BW_2_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                    elif mkr_2_param[4] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer2:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer2:Y?"))
                        mkr_2_param[1] = markerX
                        mkr_2_param[2] = markerY
                    # Delta
                    elif mkr_2_param[5] == "ON":
                        delta_distance = instrument1.query("CALC:MARK2:FUNC:DELTa:X:OFFset?")
                        delta_distance = conversions.str2float(delta_distance,delta_units)
                        markerX = conversions.str2float(str(instrument1.query("CALCulate:marker2:X?").rstrip()),delta_units)
                        markerY = float(instrument1.query("CALCulate:marker2:Y?"))
                        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:marker2:FUNC:DELta:X:REF?").rstrip()),delta_units)
                        markerYRef = float(instrument1.query("CALCulate:marker2:FUNC:DELta:Y:REF?"))
                        delta_2_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                    # OSNR
                    elif mkr_2_param[6] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer2:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer2:Y?"))
                        mkr_2_param[1] = markerX
                        mkr_2_param[2] = markerY
                        OSNRVal = float(instrument1.query("CALCulate:marker2:FUNCtion:OSNR:RESult?"))
                        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
                        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:marker2:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
                        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:marker2:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
                        if mkr_2_param[7] == 'TRA':
                            trace_data = traceA
                        elif mkr_2_param[7] == 'TRB':
                            trace_data = traceB
                        elif mkr_2_param[7] == 'TRC':
                            trace_data = traceC
                        elif mkr_2_param[7] == 'TRD':
                            trace_data = traceD
                        elif mkr_2_param[7] == 'TRE':
                            trace_data = traceE
                        elif mkr_2_param[7] == 'TRF':
                            trace_data = traceF
                        trace_x = trace_data[:,0]
                        trace_y = trace_data[:,1]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyL = trace_y[mkr_index]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyR = trace_y[mkr_index]
                        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
                        OSNRyC = float(instrument1.query("CALCulate:MARKer2:FUNCtion:OSNR:Y:CENTer?"))
                        if abs(OSNRyC) > 100:
                            OSNRyC = 0
                            OSNRVal = 0
                        OSNR_2_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal]
                else:
                    if mkr_2_param[7] == "TRA":
                        traceX = traceA[:,0]
                        traceY = traceA[:,1]
                    elif mkr_2_param[7] == "TRB":
                        traceX = traceB[:,0]
                        traceY = traceB[:,1]
                    elif mkr_2_param[7] == "TRC":
                        traceX = traceC[:,0]
                        traceY = traceC[:,1]
                    elif mkr_2_param[7] == "TRD":
                        traceX = traceD[:,0]
                        traceY = traceD[:,1]
                    elif mkr_2_param[7] == "TRE":
                        traceX = traceE[:,0]
                        traceY = traceE[:,1]
                    elif mkr_2_param[7] == "TRF":
                        traceX = traceF[:,0]
                        traceY = traceF[:,1]
                    markerX = traceX[mkr_2_index]
                    markerY = traceY[mkr_2_index]
                    mkr_2_param[1] = conversions.str2float(markerX,mkr_units)
                    mkr_2_param[2] = markerY

            if mkr_3_param[0] == "1":
                if mkr_3_extras == 1:
                    # Bandwidth
                    if mkr_3_param[3] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer3:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer3:Y?"))
                        mkr_3_param[1] = markerX
                        mkr_3_param[2] = markerY
                        trc = mkr_3_param[7]
                        xL = str(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:X:LEFT?").rstrip())
                        BWxL = conversions.str2float(xL, BW_units)
                        xR = str(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
                        BWxR = conversions.str2float(xR, BW_units)
                        xC = str(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:X:CENTer?").rstrip())
                        BWxC = conversions.str2float(xC, BW_units)
                        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer3:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
                        BWyL = mkr_3_param[2] + mkrBWY
                        BWyR = mkr_3_param[2] + mkrBWY
                        BW_3_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                    elif mkr_3_param[4] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer3:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer3:Y?"))
                        mkr_3_param[1] = markerX
                        mkr_3_param[2] = markerY
                    # Delta
                    elif mkr_3_param[5] == "ON":
                        delta_distance = instrument1.query("CALC:MARK3:FUNC:DELTa:X:OFFset?")
                        delta_distance = conversions.str2float(delta_distance,delta_units)
                        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:X?").rstrip()),delta_units)
                        markerY = float(instrument1.query("CALCulate:MARKer3:Y?"))
                        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNC:DELta:X:REF?").rstrip()),delta_units)
                        markerYRef = float(instrument1.query("CALCulate:MARKer3:FUNC:DELta:Y:REF?"))
                        delta_3_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                    # OSNR
                    elif mkr_3_param[6] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer3:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer3:Y?"))
                        mkr_3_param[1] = markerX
                        mkr_3_param[2] = markerY
                        OSNRVal = float(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:RESult?"))
                        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
                        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
                        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
                        if mkr_3_param[7] == 'TRA':
                            trace_data = traceA
                        if mkr_3_param[7] == 'TRB':
                            trace_data = traceB
                        if mkr_3_param[7] == 'TRC':
                            trace_data = traceC
                        if mkr_3_param[7] == 'TRD':
                            trace_data = traceD
                        if mkr_3_param[7] == 'TRE':
                            trace_data = traceE
                        if mkr_3_param[7] == 'TRF':
                            trace_data = traceF
                        trace_x = trace_data[:,0]
                        trace_y = trace_data[:,1]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyL = trace_y[mkr_index]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyR = trace_y[mkr_index]
                        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
                        OSNRyC = float(instrument1.query("CALCulate:MARKer3:FUNCtion:OSNR:Y:CENTer?"))
                        if abs(OSNRyC) > 100:
                            OSNRyC = 0
                            OSNRVal = 0
                        OSNR_3_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal] 
                else:
                    if mkr_3_param[7] == "TRA":
                        traceX = traceA[:,0]
                        traceY = traceA[:,1]
                    elif mkr_3_param[7] == "TRB":
                        traceX = traceB[:,0]
                        traceY = traceB[:,1]
                    elif mkr_3_param[7] == "TRC":
                        traceX = traceC[:,0]
                        traceY = traceC[:,1]
                    elif mkr_3_param[7] == "TRD":
                        traceX = traceD[:,0]
                        traceY = traceD[:,1]
                    elif mkr_3_param[7] == "TRE":
                        traceX = traceE[:,0]
                        traceY = traceE[:,1]
                    elif mkr_3_param[7] == "TRF":
                        traceX = traceF[:,0]
                        traceY = traceF[:,1]
                    markerX = traceX[mkr_3_index]
                    markerY = traceY[mkr_3_index]
                    mkr_3_param[1] = conversions.str2float(markerX,mkr_units)
                    mkr_3_param[2] = markerY

            if mkr_4_param[0] == "1":
                if mkr_4_extras == 1:
                    # Bandwidth
                    if mkr_4_param[3] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer4:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer4:Y?"))
                        mkr_4_param[1] = markerX
                        mkr_4_param[2] = markerY
                        trc = mkr_4_param[7]
                        xL = str(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:X:LEFT?").rstrip())
                        BWxL = conversions.str2float(xL, BW_units)
                        xR = str(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:X:RIGHt?").rstrip())
                        BWxR = conversions.str2float(xR, BW_units)
                        xC = str(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:X:CENTer?").rstrip())
                        BWxC = conversions.str2float(xC, BW_units)
                        mkrBWY = conversions.str2float(instrument1.query("CALCulate:MARKer4:FUNCtion:BANDwidth:NDB?"),amplitude_units)                                                        
                        BWyL = mkr_4_param[2] + mkrBWY
                        BWyR = mkr_4_param[2] + mkrBWY
                        BW_4_param = [BWxL, BWxR, BWxC, BWyL, BWyR, mkrBWY]
                    elif mkr_4_param[4] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer4:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer4:Y?"))
                        mkr_4_param[1] = markerX
                        mkr_4_param[2] = markerY
                    # Delta
                    elif mkr_4_param[5] == "ON":
                        delta_distance = instrument1.query("CALC:MARK4:FUNC:DELTa:X:OFFset?")
                        delta_distance = conversions.str2float(delta_distance,delta_units)
                        markerX = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:X?").rstrip()),delta_units)
                        markerY = float(instrument1.query("CALCulate:MARKer4:Y?"))
                        markerXRef = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNC:DELta:X:REF?").rstrip()),delta_units)
                        markerYRef = float(instrument1.query("CALCulate:MARKer4:FUNC:DELta:Y:REF?"))
                        delta_4_param = [markerX, markerY, markerXRef, markerYRef, delta_distance]
                    # OSNR
                    elif mkr_4_param[6] == "ON":
                        markerXt = float(instrument1.query("CALCulate:MARKer4:X?"))
                        markerX = conversions.str2float(markerXt, mkr_units)
                        markerY = float(instrument1.query("CALCulate:MARKer4:Y?"))
                        mkr_4_param[1] = markerX
                        mkr_4_param[2] = markerY
                        OSNRVal = float(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:RESult?"))
                        OSNRVal = conversions.str2float(OSNRVal,amplitude_units)
                        OSNRxL = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:X:LEFT?").rstrip()), mkr_units)
                        OSNRxR = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:X:RIGHt?").rstrip()), mkr_units)
                        if mkr_4_param[7] == 'TRA':
                            trace_data = traceA
                        if mkr_4_param[7] == 'TRB':
                            trace_data = traceB
                        if mkr_4_param[7] == 'TRC':
                            trace_data = traceC
                        if mkr_4_param[7] == 'TRD':
                            trace_data = traceD
                        if mkr_4_param[7] == 'TRE':
                            trace_data = traceE
                        if mkr_4_param[7] == 'TRF':
                            trace_data = traceF
                        trace_x = trace_data[:,0]
                        trace_y = trace_data[:,1]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxL)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyL = trace_y[mkr_index]
                        error_thresh = 1
                        for i in range(len(trace_x)):
                            distance_x = abs(conversions.str2float(trace_x[i],wavelength_units)-OSNRxR)
                            if distance_x < error_thresh:
                                mkr_index = i
                                error_thresh = distance_x
                        OSNRyR = trace_y[mkr_index]
                        OSNRxC = conversions.str2float(str(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
                        OSNRyC = float(instrument1.query("CALCulate:MARKer4:FUNCtion:OSNR:Y:CENTer?"))
                        if abs(OSNRyC) > 100:
                            OSNRyC = 0
                            OSNRVal = 0
                        OSNR_4_param = [OSNRxL, OSNRyL, OSNRxR, OSNRyR, OSNRxC, OSNRyC, OSNRVal] 
                else: 
                    if mkr_4_param[7] == "TRA":
                        traceX = traceA[:,0]
                        traceY = traceA[:,1]
                    elif mkr_4_param[7] == "TRB":
                        traceX = traceB[:,0]
                        traceY = traceB[:,1]
                    elif mkr_4_param[7] == "TRC":
                        traceX = traceC[:,0]
                        traceY = traceC[:,1]
                    elif mkr_4_param[7] == "TRD":
                        traceX = traceD[:,0]
                        traceY = traceD[:,1]
                    elif mkr_4_param[7] == "TRE":
                        traceX = traceE[:,0]
                        traceY = traceE[:,1]
                    elif mkr_4_param[7] == "TRF":
                        traceX = traceF[:,0]
                        traceY = traceF[:,1]
                    markerX = traceX[mkr_4_index]
                    markerY = traceY[mkr_4_index]
                    mkr_4_param[1] = conversions.str2float(markerX,mkr_units)
                    mkr_4_param[2] = markerY

