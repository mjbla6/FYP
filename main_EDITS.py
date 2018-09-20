## REPLACE GUI_MARKERSETUPWINDOW WITH NEW ONE


## TO GO IN SETUP FUNCTION
        global mkr_units
        mkr_units = 'nm'

        global BW_units
        BW_units = 'nm'

        global delta_units
        delta_units = 'nm'

        global mkrInterpOnOff
        mkrInterpOnOff = str(my_instrument.query("CALCulate:MARKer:INTerpolation?")).rstrip()
        if mkrInterpOnOff == '0':
            mkrInterpOnOff = 'OFF'
        elif mkrInterpOnOff == '1':
            mkrInterpOnOff = 'ON'

        global BWInterpOnOff
        BWInterpOnOff = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:INTerpolation?" %active_marker)).rstrip()
        if BWInterpOnOff == '0':
            BWInterpOnOff = 'OFF'
        elif BWInterpOnOff == '1':
            BWInterpOnOff = 'ON'

        global mkrThreshOnOff
        mkrThreshOnOff = str(my_instrument.query("CALCulate:THReshold:STATe?")).rstrip()
        if mkrThreshOnOff == '0':
            mkrThreshOnOff = 'OFF'
        elif mkrThreshOnOff == '1':
            mkrThreshOnOff = 'ON'

        global userMkrThresh
        if mkrThreshOnOff == '1':
            userMkrThresh = str(my_instrument.query("CALCulate:THReshold?")).rstrip()
        else:
            userMkrThresh = '0'

        global noiseMkrBW
        noiseMkrBW = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:NOISe:BANDwidth?" %active_marker)).rstrip()

        global OSNRType
        OSNRType = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:OSNR:MODE?" %active_marker)).rstrip()

        global OSNROffset
        if OSNRType == 'MAN':
            OSNROffset = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:OSNR:OFFSet" %active_marker)).rstrip()
        else:
            OSNROffset = '0'

        global peakExcur
        peakExcur = str(my_instrument.query("CALCulate:MARKer%s:PEXCursion:PEAK?" %active_marker)).rstrip()

        global pitExcur
        pitExcur = str(my_instrument.query("CALCulate:MARKer%s:PEXCursion:PIT?" %active_marker)).rstrip()


## REPLACE CLASS WITH BELOW:
class MarkerSetup(QtWidgets.QDialog, Ui_markerSetupWindow):
    def __init__(self, MkrNo, parent=None):
        super(MarkerSetup, self).__init__(parent)
        self.setupUi(self)

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
        self.menuOSNR.addAction("PM", self.OSNRAction1)
        self.menuOSNR.addAction("Auto", self.OSNRAction2)
        self.menuOSNR.addAction("Manual", self.OSNRAction3)
        self.buttonOSNR.setMenu(self.menuOSNR)

        self.linePeakExcur.setText("%s" %peakExcur)
        self.linePitExcur.setText("%s" %pitExcur)
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
        self.buttonOSNR.setText("PM")
        self.lineOSNR.setText("DISABLED")

    def OSNRAction2(self):
        self.buttonOSNR.setText("AUTO")
        self.lineOSNR.setText("DISABLED")

    def OSNRAction3(self):
        self.buttonOSNR.setText("MAN")
        self.lineOSNR.setText("%s" %OSNROffset)
        self.lineOSNR.setValidator(validator)

    def onAccept(self):
        mkr_units = str(self.buttonNormMkrUnits.text()).rstrip()
        delta_units = str(self.buttonDeltaMkrUnits.text()).rstrip()
        BW_units = str(self.buttonBWMkrUnits.text()).rstrip()

        if self.buttonMkrInterp.text() == "ON":
            mkrInterpOnOff = 'ON'
            my_instrument.write("CALCulate:MARKer%s:INT 1" %active_marker)
        else:
            mkrInterpOnOff = 'OFF'
            my_instrument.write("CALCulate:MARKer%s:INT 0" %active_marker)

        if self.buttonBWMkrInterp.text() == "ON":
            BWInterpOnOff = 'ON'
            my_instrument.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:INTerpolation 1" %active_marker)
        else:
            BWInterpOnOff = 'OFF'
            my_instrument.write("CALCulate:MARKer%s:FUNCtion:BANDwidth:INTerpolation 0" %active_marker)

        peakExcur = str(self.linePeakExcur.text()).rstrip()
        my_instrument.write("CALCulate:MARKer%s:PEXCursion:PEAK %sdB" %peakExcur)

        pitExcur = str(self.linePitExcur.text()).rstrip()
        my_instrument.write("CALCulate:MARKer%s:PEXCursion:PIT %sdB" %pitExcur)

        if self.buttonUserMkrThresh.text() == "ON":
            mkrThreshOnOff = 'ON'
            my_instrument.write("CALCulate:THReshold:STATe 1")
            userMkrThresh = str(self.lineSrchThresh.text()).rstrip()
            my_instrument.write("CALCulate:THReshold %sdBm" %userMkrThresh)
        else:
            mkrThreshOnOff = 'OFF'
            my_instrument.write("CALCulate:THReshold:STATe 0")

        if self.buttonNoiseMkrBW.text() == "0.1 nm":
            noiseMkrBW = '0.1'
        else:
            noiseMkrBW = '1.0'

        if self.buttonOSNR.text() == "MAN":
            OSNRType = 'MAN'
            my_instrument.write("CALCulate:MARKer%s:FUNCtion:OSNR:MODE %s" %(active_marker, OSNRType))
            OSNROffset = str(self.lineOSNR.text()).rstrip()
            my_instrument.write("CALCulate:MARKer%s:FUNCtion:OSNR:OFFSet %snm" %(active_marker, OSNROffset))
        elif self.buttonOSNR.text() == "AUTO":
            OSNRType = 'AUTO'
        else:
            OSNRType = 'PM'


    def onReject(self):
        return