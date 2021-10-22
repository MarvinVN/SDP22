import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

class MainWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()
		# add title of game
		self.setWindowTitle("BLACKJACK")

		# set vertical box layout
		self.setLayout(qtw.QVBoxLayout())

		# create a label for the title screen of game
		title_label = qtw.QLabel("JACKBLACK!")

		# change the font, position and size of label
		title_label.setFont(qtg.QFont('Helvetica', 25))
		# title_label.setSizePolicy(qtc.QSizePolicy.Expanding, qtc.QSizePolicy.Expanding)
		# title_label.setAlignment(qtc.AlignCenter)
		self.layout().addWidget(title_label)

		# create a button to start the game
		start_game_button = qtw.QPushButton("START GAME",
			clicked = lambda: press_it())
		self.layout().addWidget(start_game_button)
		#hi marvin



		# show the app
		self.show()

		def press_it():
			# do nothing
			title_label.setText("Congrats! Button was pressed.")
			self.layout().itemAt(1).widget().deleteLater() # deletes the widget at index 1 (button)

"""
		def press_it():
			# this only hides the widgets, rather than removing them
			# need to fix this later on, so that it is visually accurate
			# need to put these functions into their own proper function/class 
			#		(not in the button press function)
			title_label.clear()
			start_game_button.hide()
			num_players_label = qtw.QLabel("Select number of players:")
			num_players_label.setFont(qtg.QFont('Helvetica', 18))
			self.layout().addWidget(num_players_label)

			# create a combo box
			num_players_combo_box = qtw.QComboBox(self,
				editable = False,
				insertPolicy = qtw.QComboBox.InsertAtTop) # or InsertAtBottom

			# add number of player options to combo box
			num_players_combo_box.addItems(["1", "2", "3", "4"])

			# put combo box on screen
			self.layout().addWidget(num_players_combo_box)

			# add selection button
			num_players_selection_button = qtw.QPushButton("Enter",
				clicked = lambda: press_it2(num_players_selection_button, num_players_combo_box, 
					num_players_label))
			self.layout().addWidget(num_players_selection_button)


		def press_it2(num_players_selection_button, num_players_combo_box, num_players_label):
			num_players_selection_button.hide()
			num_players_combo_box.hide()
			num_players_label.clear()
			# add player names
			player_names_label = qtw.QLabel("Add player names:")
			player_names_label.setFont(qtg.QFont('Helvetica', 18))

			# create a combo box for player names
			player_names_combo_box = qtw.QComboBox(self,
				editable = True,
				insertPolicy = qtw.QComboBox.InsertAtTop) # or InsertAtBottom
			# add items to the combo box
			# need to retrict the number of input names to the number of players user chose
			player_names_combo_box.addItem("[insert player name]")

			# add button to enter
			player_names_enter_button = qtw.QPushButton("Enter",
				clicked = lambda: press_it3())

			# put widgets on screen
			self.layout().addWidget(player_names_label)
			self.layout().addWidget(player_names_combo_box)
			self.layout().addWidget(player_names_enter_button)


		def press_it3():
			# clear the entire widget layout
			for i in reversed(range(self.layout().count())):
				self.layout().itemAt(i).widget().setParent(None)



"""

app = qtw.QApplication([])
mw = MainWindow()

# Run the app
app.exec_()