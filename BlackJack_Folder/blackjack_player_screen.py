import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

# add Marvin's gaming algorithms to this file
# have Marvin's code in separate file and call functions into this file

class PlayerScreen(qtw.QWidget):
	def __init__(self):
		super().__init__()
		# add title of game
		self.setWindowTitle("Player Screen")

		# set grid box layout
		self.setLayout(qtw.QGridLayout())

		# menu combo box
		self.menu_combo_box = qtw.QComboBox(self,
			insertPolicy = qtw.QComboBox.InsertAtTop)
		self.menu_combo_box.addItems(["MENU:","rules", "card guide", "end game", "other"])
		self.layout().addWidget(self.menu_combo_box, 0, 0)

		# label for dealer
		self.dealer_card_label = qtw.QLabel("Dealer Cards:")
		self.dealer_card_label.setObjectName("dealer_cards")
		self.layout().addWidget(self.dealer_card_label, 0, 1)

		# label for amount left
		self.total_amount_label = qtw.QLabel("$ AMOUNT LEFT $")
		self.total_amount_label.setObjectName("amount_left")
		self.layout().addWidget(self.total_amount_label, 0, 2)

		# label for player cards
		self.player_card_label = qtw.QLabel("Player Cards:")
		self.player_card_label.setObjectName("player_cards")
		self.layout().addWidget(self.player_card_label, 1, 1)

		# label for current bet
		self.current_bet_label = qtw.QLabel("Current Bet:")
		self.current_bet_label.setObjectName("current_bet")
		self.layout().addWidget(self.current_bet_label, 1, 0)

		# vertical box for button press
		self.vbox = qtw.QVBoxLayout()
		self.hit_button = qtw.QPushButton("HIT")
		self.double_button = qtw.QPushButton("DOUBLE")
		self.stand_button = qtw.QPushButton("STAND")
		self.vbox.addWidget(self.hit_button)
		self.vbox.addWidget(self.double_button)
		self.vbox.addWidget(self.stand_button)

		self.layout().addLayout(self.vbox, 1, 2)


		self.show()

app = qtw.QApplication([])
ps = PlayerScreen()

# Run the app
app.exec_()