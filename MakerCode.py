   marker_data_array = ''


class Agilent86142B(QtWidgets.QWidget, Ui_Agilent86142B):
    def __init__(self, parent=None):
        super(Agilent86142B, self).__init__(parent)
        self.textDisplay()

   def setupInstrument(self):
        global marker_data_array
        marker_data_array[0] = str(my_instrument.query("CALCulate:MARKer1:X?")).rstrip()
        marker_data_array[1] = str(my_instrument.query("CALCulate:MARKer1:Y?")).rstrip()
        marker_data_array[2] = str(my_instrument.query("CALCulate:MARKer2:X?")).rstrip()
        marker_data_array[3] = str(my_instrument.query("CALCulate:MARKer2:Y?")).rstrip()
        marker_data_array[4] = str(my_instrument.query("CALCulate:MARKer3:X?")).rstrip()
        marker_data_array[5] = str(my_instrument.query("CALCulate:MARKer3:Y?")).rstrip()
        marker_data_array[6] = str(my_instrument.query("CALCulate:MARKer4:X?")).rstrip()
        marker_data_array[7] = str(my_instrument.query("CALCulate:MARKer4:Y?")).rstrip()



    def textDisplay(self):
        if active_marker_matrix[0] == "1":
            self.topLabel11.setText("Mkr 1 (T)")
            self.topLabel12.setText("%s %s" %(marker_data_array[0],wavelength_units))
            self.topLabel13.setText("%s %s" %(marker_data_array[1],amplitude_units))

        if active_marker_matrix[1] == "1":
            self.topLabel21.setText("Mkr 2 (T)")
            self.topLabel22.setText("%s %s" %(marker_data_array[2],wavelength_units))
            self.topLabel23.setText("%s %s" %(marker_data_array[3],amplitude_units))

        if active_marker_matrix[0] == "1":
            if active_marker_matrix[1] == "1":
                self.topLabel31.setText("Mkr 2-1")
                markerDiffWL = marker_data_array[2]-marker_data_array[0]
                markerDiffAmp = marker_data_array[3]-marker_data_array[1]
                self.topLabel32.setText("%s %s" %(markerDiffWL,wavelength_units))
                self.topLabel33.setText("%s %s" %(markerDiffAmp,amplitude_units))
                
        if active_marker_matrix[2] == "1":
            self.topLabel41.setText("Mkr 3 (T)")
            self.topLabel42.setText("%s %s" %(marker_data_array[4],wavelength_units))
            self.topLabel43.setText("%s %s" %(marker_data_array[5],amplitude_units))

        if active_marker_matrix[3] == "1":
            self.topLabel51.setText("Mkr 4 (T)")
            self.topLabel52.setText("%s %s" %(marker_data_array[6],wavelength_units))
            self.topLabel53.setText("%s %s" %(marker_data_array[7],amplitude_units))

        if active_marker_matrix[2] == "1":
            if active_marker_matrix[3] == "1":
                self.topLabel61.setText("Mkr 4-3")
                markerDiffWL = marker_data_array[6]-marker_data_array[4]
                markerDiffAmp = marker_data_array[7]-marker_data_array[5]
                self.topLabel62.setText("%s %s" %(markerDiffWL,wavelength_units))
                self.topLabel63.setText("%s %s" %(markerDiffAmp,amplitude_units))