	def trceMath(self):
		self.clearLayout(self.subButtonLayout)

		self.buttonDefMathTrcC = QtWidgets.QPushButton("Default Math Trace C", self)
		self.menuTrcMathC = QtWidgets.QMenu()
		self.menuTrcMathC.addAction("Log: C = A-B", self.TrcMathCAction1)
		self.menuTrcMathC.addAction("Log: C = A+B", self.TrcMathCAction2)
		self.menuTrcMathC.addAction("Lin: C = A-B", self.TrcMathCAction3)
		self.menuTrcMathC.addAction("Lin: C = A+B", self.TrcMathCAction4)
		self.menuTrcMathC.addAction("Trace C Math Off", self.TrcMathCAction5)
		self.buttonDefMathTrcC.setMenu(self.menuTrcMathC)
		self.subButtonLayout.addWidget(self.buttonDefMathTrcC)
		self.buttonDefMathTrcF = QtWidgets.QPushButton("Default Math Trace F", self)
		self.menuTrcMathF = QtWidgets.QMenu()
		self.menuTrcMathF.addAction("Log: F = C-D", self.TrcMathFAction1)
		self.menuTrcMathF.addAction("Trace F Math Off", self.TrcMathFAction2)
		self.buttonDefMathTrcF.setMenu(self.menuTrcMathF)
		self.subButtonLayout.addWidget(self.buttonDefMathTrcF)
		self.buttonExchMenu = QtWidgets.QPushButton("Exchange Menu", self)
		self.menuExchange = QtWidgets.QMenu()
		self.menuExchange.addAction("A Exchange B", self.ExchangeAction1)
		self.menuExchange.addAction("B Exchange C", self.ExchangeAction2)
		self.menuExchange.addAction("C Exchange A", self.ExchangeAction3)
		self.menuExchange.addAction("D Exchange A", self.ExchangeAction4)
		self.menuExchange.addAction("E Exchange A", self.ExchangeAction5)
		self.menuExchange.addAction("F Exchange A", self.ExchangeAction6)
		self.buttonExchMenu.setMenu(self.menuExchange)
		self.subButtonLayout.addWidget(self.buttonExchMenu)
		self.buttonTrceOffset = QtWidgets.QPushButton("Trace Offset", self)
		self.subButtonLayout.addWidget(self.buttonTrceOffset)
		self.buttonBlank = QtWidgets.QPushButton("", self)
		self.subButtonLayout.addWidget(self.buttonBlank)
		self.buttonAllMathOff = QtWidgets.QPushButton("All Math Off", self)
		self.subButtonLayout.addWidget(self.buttonAllMathOff)
		self.buttonPrevMenu = QtWidgets.QPushButton("Previous Menu", self)
		self.subButtonLayout.addWidget(self.buttonPrevMenu)

		self.buttonPrevMenu.clicked.connect(self.tracesMenu)

	def TrcMathCAction1(self):
		return

	def TrcMathCAction2(self):
		return

	def TrcMathCAction3(self):
		return

	def TrcMathCAction4(self):
		return

	def TrcMathCAction5(self):
		return

	def TrcMathFAction1(self):
		return

	def TrcMathFAction2(self):
		return

	def ExchangeAction1(self):
		return

	def ExchangeAction2(self):
		return

	def ExchangeAction3(self):
		return

	def ExchangeAction4(self):
		return

	def ExchangeAction5(self):
		return

	def ExchangeAction6(self):
		return