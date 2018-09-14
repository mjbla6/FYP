class NewMarkerWindow(QtWidgets.QDialog, Ui_newMarkerWindow):
	def __init__(self, parent=None):
		super(NewMarkerWindow, self).__init__(parent)
		self.setupUi(self)

		self.buttonMkrSel.setText("Mkr 1")
		self.menuMkrSel = QtWidgets.QMenu()
		self.menuMkrSel.addAction("Mkr 1", self.MkrSelAction1)
		self.menuMkrSel.addAction("Mkr 2", self.MkrSelAction2)
		self.menuMkrSel.addAction("Mkr 3", self.MkrSelAction3)
		self.menuMkrSel.addAction("Mkr 4", self.MkrSelAction4)
		self.buttonMkrSel.setMenu(self.menuMkrSel)
		self.buttonTrcSel.setText("Trace A")
		self.menuTrcSel = QtWidgets.QMenu()
		self.menuTrcSel.addAction("Trace A", self.TrcSelAction1)
		self.menuTrcSel.addAction("Trace B", self.TrcSelAction2)
		self.menuTrcSel.addAction("Trace C", self.TrcSelAction3)
		self.menuTrcSel.addAction("Trace D", self.TrcSelAction4)
		self.menuTrcSel.addAction("Trace E", self.TrcSelAction5)
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