import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

class GamePlaySettings(qtw.QWidget):
	def __init__(self):
		super().__init__()
		# add title of game
		self.setWindowTitle("GAME PLAY SETTINGS")

		# set vertical box layout
		self.setLayout(qtw.QVBoxLayout())

		# set grid box layout
		self.gbox1 = qtw.QGridLayout()
		self.gbox2 = qtw.QGridLayout()

		# label for confirmation
		self.pressed_continue_label = qtw.QLabel("Confirm these settings?")
		self.pressed_continue_label.setObjectName("confirm")

		# create a label for the screen
		self.title_label = qtw.QLabel("Game Play Settings")
		# change the font, position and size of label
		self.title_label.setFont(qtg.QFont('Helvetica', 25))
		self.layout().addWidget(self.title_label)

		####### grid layout info #######
		# create label for number of players
		self.num_players_label = qtw.QLabel("Number of Players:")
		self.gbox1.addWidget(self.num_players_label, 0, 0)

		# create a combo box of number of player options
		self.num_players_combo_box = qtw.QComboBox(self,
			insertPolicy = qtw.QComboBox.InsertAtTop) # or InsertAtBottom

		# add number of player options to combo box
		self.num_players_combo_box.addItems(["1", "2", "3", "4"])

		self.gbox1.addWidget(self.num_players_combo_box, 0, 1)

		# create label for starting amount
		self.start_amount_label = qtw.QLabel("Starting Amount (in dollars):")
		self.gbox1.addWidget(self.start_amount_label, 1, 0)

		# create combo box for starting amount
		# change this layout later to be functioned using arrow buttons
		self.start_amount_combo_box = qtw.QComboBox(self,
			insertPolicy = qtw.QComboBox.InsertAtTop)

		# add amount options to combo box
		for i in range(10):
			val = i * 100
			self.start_amount_combo_box.addItem(str(val))

		# put combo box on screen
		self.gbox1.addWidget(self.start_amount_combo_box, 1, 1)

		# create label for MODE of game play
		self.mode_label = qtw.QLabel("Game Mode (select 1):")
		self.gbox1.addWidget(self.mode_label, 2, 0)
		#create combo box for mode options
		self.mode_combo_box = qtw.QComboBox(self,
			insertPolicy = qtw.QComboBox.InsertAtTop)

		# options for mode
		self.mode_combo_box.addItem('Total Winnings', '[enter winning amount]')
		self.mode_combo_box.addItem('Number of Wins', '[enter number of wins]')
		self.mode_combo_box.addItem('Total Games', '[enter number of games to play]')
		self.mode_combo_box.addItem('Duration', '[enter duration of time (in minutes)]')
		self.gbox1.addWidget(self.mode_combo_box, 2, 1)

		self.layout().addLayout(self.gbox1)

		self.entry_box = qtw.QLineEdit()
		self.layout().addWidget(self.entry_box)

		self.mode_combo_box.currentIndexChanged.connect(self.updateEntryMode)

		self.updateEntryMode(self.mode_combo_box.currentIndex())

		# add button to move on
		self.continue_button = qtw.QPushButton("CONTINUE")
			#clicked = lambda: self.clearLayout(self.layout()))

		#self.continue_button.clicked.connect(lambda: self.clearLayout(self.layout()))
		self.continue_button.clicked.connect(lambda: self.message())

		#self.continue_button.clicked.connect(lambda: self.message())
		self.layout().addWidget(self.continue_button)
		self.layout().addWidget(self.pressed_continue_label)
		self.pressed_continue_label.hide()




		#self.continue_button.clicked.connect(self.message)



		self.show()

	def updateEntryMode(self, index):
		self.entry_box.setText("")
		entry = self.mode_combo_box.itemData(index)
		if entry:
			self.entry_box.setText(str(entry))

	def clearLayout(self, layout):
		if layout is not None:
			while layout.count():
				item = layout.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.clearLayout(item.layout())

	def message(self):
		#self.pressed_continue_label = qtw.QLabel("Confirm these settings?")
		#self.title_label.setText("Congrats! You pressed CONTINUE!")
		
		self.pressed_continue_label.show()
		self.no_button = qtw.QPushButton("NO")
		self.no_button.clicked.connect(lambda: self.no_button_clicked())
		self.yes_button = qtw.QPushButton("YES")
		self.yes_button.clicked.connect(lambda: self.yes_button_clicked())


		self.gbox2.addWidget(self.no_button, 0, 0)
		self.gbox2.addWidget(self.yes_button, 0, 1)
		self.layout().addLayout(self.gbox2)


	def no_button_clicked(self):
		self.pressed_continue_label.hide()
		self.no_button.hide()
		self.yes_button.hide()


	def yes_button_clicked(self):
		if self.layout() is not None:
			while self.layout().count():
				item = self.layout().takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.clearLayout(item.layout())


app = qtw.QApplication([])
gps = GamePlaySettings()

# Run the app
app.exec_()