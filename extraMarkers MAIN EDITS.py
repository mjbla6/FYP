## REPLACE MARKER SECTION IN SETUP INSTRUMENT
## ------------------------------------------
##              MARKER PARAMETERS
## ------------------------------------------
        
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
        global BW_1_param
        global BW_2_param
        global BW_3_param
        global BW_4_param
        global mkrExtraFlag
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        mkr_1_param = [0, 0, 0, '0', '0', '0', '0', '0']
        mkr_2_param = [0, 0, 0, '0', '0', '0', '0', '0']
        mkr_3_param = [0, 0, 0, '0', '0', '0', '0', '0']
        mkr_4_param = [0, 0, 0, '0', '0', '0', '0', '0']
        ## bw_x_param = [xL, XR, yL, yR, xDifference]
        BW_1_param = [0, 0, 0, 0, 0]
        BW_2_param = [0, 0, 0, 0, 0]
        BW_3_param = [0, 0, 0, 0, 0]
        BW_4_param = [0, 0, 0, 0, 0]

        for i in range(1,5):
            if i == 1:
                itrac = "1"
            if i == 2:
                itrac = "2"
            if i == 3:
                itrac = "3"
            if i == 4:
                itrac = "4"

            mkrOnOff = str(my_instrument.query("CALCulate:MARKer%s:STATe?" %itrac)).rstrip()

            markerBWOnOff = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:BANDwidth:STATe?" %itrac)).rstrip()
            if markerBWOnOff == "1":
                markerBWOnOff = "ON"
            elif markerBWOnOff == "0":
                markerBWOnOff = "OFF"

            noiseMarkOnOff = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:NOISe:STATe?" %itrac)).rstrip()
            if noiseMarkOnOff == "1":
                noiseMarkOnOff = "ON"
            elif noiseMarkOnOff == "0":
                noiseMarkOnOff = "OFF"

            deltaMarkOnOff = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:DELTa:STATe?" %itrac)).rstrip()
            if deltaMarkOnOff == "1":
                deltaMarkOnOff = "ON"
            elif deltaMarkOnOff == "0":
                deltaMarkOnOff = "OFF"

            osnrMarkOnOff = str(my_instrument.query("CALCulate:MARKer%s:FUNCtion:DELTa:STATe?" %itrac)).rstrip()
            if osnrMarkOnOff == "1":
                osnrMarkOnOff = "ON"
            elif osnrMarkOnOff == "0":
                osnrMarkOnOff = "OFF"

            mkrTrc = str(my_instrument.query("CALCulate:MARKer%s:TRACe?" %itrac)).rstrip()

            if itrac == '1':
                mkr_1_param[3] = markerBWOnOff
                mkr_1_param[4] = noiseMarkOnOff
                mkr_1_param[5] = deltaMarkOnOff
                mkr_1_param[6] = osnrMarkOnOff
                mkr_1_param[7] = mkrTrc
            if itrac == '2':
                mkr_2_param[3] = markerBWOnOff
                mkr_2_param[4] = noiseMarkOnOff
                mkr_2_param[5] = deltaMarkOnOff
                mkr_2_param[6] = osnrMarkOnOff
                mkr_2_param[7] = mkrTrc
            if itrac == '3':
                mkr_3_param[3] = markerBWOnOff
                mkr_3_param[4] = noiseMarkOnOff
                mkr_3_param[5] = deltaMarkOnOff
                mkr_3_param[6] = osnrMarkOnOff
                mkr_3_param[7] = mkrTrc
            if itrac == '4':
                mkr_4_param[3] = markerBWOnOff
                mkr_4_param[4] = noiseMarkOnOff
                mkr_4_param[5] = deltaMarkOnOff
                mkr_4_param[6] = osnrMarkOnOff
                mkr_4_param[7] = mkrTrc

            if itrac == '1':
                mkr_1_param[0] = mkrOnOff
                self.mkr1Display()
            if itrac == '2':
                mkr_2_param[0] = mkrOnOff
                self.mkr2Display()
            if itrac == '3':
                mkr_3_param[0] = mkrOnOff
                self.mkr3Display()
            if itrac == '4':
                mkr_4_param[0] = mkrOnOff
                self.mkr4Display()

        global active_mkr_param
        active_mkr_param = [0, 0, 0, '0', '0', '0', '0', '0']
        global active_BW_param
        active_BW_param = [0, 0, 0, 0, 0]

        if mkr_1_param[0] == '1':
            active_marker = '1'
        if mkr_2_param[0] == '1':
            active_marker = '2'
        if mkr_3_param[0] == '1':
            active_marker = '3'
        if mkr_4_param[0] == '1':
            active_marker = '4'
        print("Active Mkr: %s" %active_marker)

        if active_marker == '1':
            active_mkr_param = mkr_1_param
            self.mkr1Display()
        if active_marker == '2':
            active_mkr_param = mkr_2_param
            self.mkr2Display()
        if active_marker == '3':
            active_mkr_param = mkr_3_param
            self.mkr3Display()
        if active_marker == '4':
            active_mkr_param = mkr_4_param
            self.mkr4Display()

        print(mkr_1_param)
        print(mkr_2_param)
        print(mkr_3_param)
        print(mkr_4_param)
        
        if mkrExtraFlag == 0:
            self.mkrCompDisplay()


## REPLACE UPDATE MKR PARAM
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

## REPLACE ACT MKRS GBLS
    def ActMkrGbl1(self):
        self.buttonActMkrGbl.setText("Mkr 1")
        global active_marker
        active_marker = '1'
        global mkr_1_param
        mkr_1_param[0] = '1'
        global active_mkr_param
        active_mkr_param = mkr_1_param
        my_instrument.write("CALCulate:MARKer1:STATe ON")
        self.mkr1Display()
        if mkrExtraFlag == 0:
            self.mkrCompDisplay()
        global menuFlag
        if menuFlag == 1:
            self.markersMenu()
        if menuFlag == 2:
            self.moreMkrFunc()

    def ActMkrGbl2(self):
        self.buttonActMkrGbl.setText("Mkr 2")
        global active_marker
        active_marker = '2'
        global mkr_2_param
        mkr_2_param[0] = '1'
        global active_mkr_param
        active_mkr_param = mkr_2_param
        my_instrument.write("CALCulate:MARKer2:STATe ON")
        self.mkr2Display()
        if mkrExtraFlag == 0:
            self.mkrCompDisplay()
        global menuFlag
        if menuFlag == 1:
            self.markersMenu()
        if menuFlag == 2:
            self.moreMkrFunc()

    def ActMkrGbl3(self):
        self.buttonActMkrGbl.setText("Mkr 3")
        global active_marker
        active_marker = '3'
        global mkr_3_param
        mkr_3_param[0] = '1'
        global active_mkr_param
        active_mkr_param = mkr_3_param
        my_instrument.write("CALCulate:MARKer3:STATe ON")
        self.mkr3Display()
        if mkrExtraFlag == 0:
            self.mkrCompDisplay()
        global menuFlag
        if menuFlag == 1:
            self.markersMenu()
        if menuFlag == 2:
            self.moreMkrFunc()

    def ActMkrGbl4(self):
        self.buttonActMkrGbl.setText("Mkr 4")
        global active_marker
        active_marker = '4'
        global mkr_4_param
        mkr_4_param[0] = '1'
        global active_mkr_param
        active_mkr_param = mkr_4_param
        my_instrument.write("CALCulate:MARKer4:STATe ON")
        self.mkr4Display()
        if mkrExtraFlag == 0:
            self.mkrCompDisplay()
        global menuFlag
        if menuFlag == 1:
            self.markersMenu()
        if menuFlag == 2:
            self.moreMkrFunc()

## ADD IN CLEAR FUNCTIONS AND REPLACE MKR DISPLAYS - WILL NEED TO CHECK IF MKR 1 WORKS AND THEN ADAPT FOR MKRS 2-4
## THEN WILL NEED TO ADD TO THE MKRSDISPLAY/PLOT FUNCTION TO DRAW THE ADDITIONAL MARKERS ON PLOT
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


    def mkr1Display(self):
        global mkr_1_param
        global BW_1_param
        global mkrExtraFlag
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_1_param[0] == "1":
            markerX = conversions.str2float(str(my_instrument.query("CALCulate:MARKer1:X?").rstrip()), mkr_units)
            markerY = float(my_instrument.query("CALCulate:MARKer1:Y?"))
            trc = mkr_1_param[7]
            self.topLabel11.setText("Mkr 1 (%s)" %trc[2])
            self.topLabel12.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel13.setText("%.2f %s" %(markerY, amplitude_units))
            if active_marker = "1":
                if mkr_1_param[3] = "1":
                    ## BW Marker
                    mkrExtraFlag = 1
                    BWxL = conversions.str2float(str(my_instrument.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:LEFT?").rstrip()), BW_units)
                    BWxR = conversions.str2float(str(my_instrument.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:RIGHt?").rstrip()), BW_units)
                    BWxC = conversions.str2float(str(my_instrument.query("CALCulate:MARKer1:FUNCtion:BANDwidth:X:CENTer?").rstrip()), BW_units)
                    BWyL = float(my_instrument.query("CALCulate:MARKer1:FUNCtion:BANDwidth:Y:LEFT?"))
                    BWyR = float(my_instrument.query("CALCulate:MARKer1:FUNCtion:BANDwidth:Y:RIGHt?"))
                    BWdiff = float(my_instrument.query("CALCulate:MARKer1:FUNCtion:BANDwidth:RESult?"))
                    self.topLabel21.setText("Mkr 1L")
                    self.topLabel22.setText("%.2f %s" %(BWxL, BW_units))
                    self.topLabel23.setText("%.2f %s" %(BWyL, amplitude_units))
                    self.topLabel31.setText("Mkr 1R")
                    self.topLabel32.setText("%.2f %s" %(BWxR, BW_units))
                    self.topLabel33.setText("%.2f %s" %(BWyR, amplitude_units))
                    self.topLabel41.setText("BW")
                    self.topLabel42.setText("%.2f %s" %(BWdiff, BW_units))
                    BWlvl = BW_1_param[4]
                    self.topLabel43.setText("%.2f %s" %(BWlvl, amplitude_units))
                    self.topLabel51.setText("CWL")
                    self.topLabel52.setText("%.2f %s" %(BWxC, BW_units))
                    self.topLabel53.setText("")
                    self.clearTopText6()
                    BW_1_param = [BWxL, BWxR, BWxC, BWyL, BWyR, BWlvl]
                elif mkr_1_param[4] = "1":
                    ## Noise Marker
                    mkrExtraFlag = 1
                    self.topLabel13.setText("%.2f %s/%snm" %(markerY, amplitude_units, noiseMkrBW))
                elif mkr_1_param[5] = "1":
                    ## Delta Marker
                    mkrExtraFlag = 1
                    ## Needs to take in value from delta marker dialog box and calculate delta marker position
                elif mkr_1_param[6] = "1":
                    ## OSNR Marker
                    OSNRx = conversions.str2float(str(my_instrument.query("CALCulate:MARKer1:FUNCtion:OSNR:X:CENTer?").rstrip()), mkr_units)
                    OSNRy = float(my_instrument.query("CALCulate:MARKer1:FUNCtion:OSNR:Y:CENTer?"))
                    OSNRVal = float(my_instrument.query("CALCulate:MARKer1:FUNCtion:OSNR:RESult?"))
                    self.clearTopText2()
                    self.topLabel31.setText("Center")
                    self.topLabel32.setText("%.2f %s" %(OSNRx, mkr_units))
                    self.topLabel33.setText("%.2f %s" %(OSNRy, amplitude_units))
                    self.clearTopText4()
                    self.topLabel51.setText("OSNR")
                    self.topLabel52.setText("OSNRVal")
                    self.topLabel53.setText("")
                    self.clearTopText6()
        else:
            mkrExtraFlag = 0
            markerX = 0
            markerY = 0
            self.topLabel11.setText("")
            self.topLabel12.setText("")
            self.topLabel13.setText("")
        mkr_1_param[1] = markerX
        mkr_1_param[2] = markerY


    def mkr2Display(self):
        global mkr_2_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_2_param[0] == "1":
            markerX = conversions.str2float(str(my_instrument.query("CALCulate:MARKer2:X?").rstrip()), mkr_units)
            markerY = float(my_instrument.query("CALCulate:MARKer2:Y?"))
            trc = mkr_2_param[7]
            self.topLabel21.setText("Mkr 2 (%s)" %trc[2])
            self.topLabel22.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel23.setText("%.2f %s" %(markerY, amplitude_units))
        else:
            markerX = 0
            markerY = 0
            self.topLabel21.setText("")
            self.topLabel22.setText("")
            self.topLabel23.setText("")
        mkr_2_param[1] = markerX
        mkr_2_param[2] = markerY


    def mkr3Display(self):
        global mkr_3_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_3_param[0] == "1":
            markerX = conversions.str2float(str(my_instrument.query("CALCulate:MARKer3:X?").rstrip()), mkr_units)
            markerY = float(my_instrument.query("CALCulate:MARKer3:Y?"))
            trc = mkr_3_param[7]
            self.topLabel41.setText("Mkr 3 (%s)" %trc[2])
            self.topLabel42.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel43.setText("%.2f %s" %(markerY, amplitude_units))
        else:
            markerX = 0
            markerY = 0
            self.topLabel41.setText("")
            self.topLabel42.setText("")
            self.topLabel43.setText("")
        mkr_3_param[1] = markerX
        mkr_3_param[2] = markerY


    def mkr4Display(self):
        global mkr_4_param
        ## mkr_x_param = [ON/OFF, X, Y, BWOnOff, NoiseOnOff, DeltaOnOff, OSNROnOff, TRACE]
        if mkr_4_param[0] == "1":
            markerX = conversions.str2float(str(my_instrument.query("CALCulate:MARKer4:X?").rstrip()), mkr_units)
            markerY = float(my_instrument.query("CALCulate:MARKer4:Y?"))
            trc = mkr_4_param[7]
            self.topLabel51.setText("Mkr 4 (%s)" %trc[2])
            self.topLabel52.setText("%.2f %s" %(markerX, mkr_units))
            self.topLabel53.setText("%.2f %s" %(markerY, amplitude_units))
        else:
            markerX = 0
            markerY = 0
            self.topLabel51.setText("")
            self.topLabel52.setText("")
            self.topLabel53.setText("")
        mkr_4_param[1] = markerX
        mkr_4_param[2] = markerY