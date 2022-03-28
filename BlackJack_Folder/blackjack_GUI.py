###################################################################
###################################################################
##########                                               ##########
##########       The contents of this file solely        ##########
##########       create the GUI and GUI functions.       ##########
##########       The game process child is also          ##########
##########       forked within this file.                ##########
##########                                               ##########
###################################################################
###################################################################


from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import blackjack
from blackjack_globals import Message
import multiprocessing as mp
import blackjack_buttons as bjb
from RPi import GPIO

# DIMENSIONS OF TOUCH DISPLAY
HEIGHT = 480
WIDTH = 800

# TIME DELAY (IN MILLISECONDS)
DELAYED = 1500

# GAME ENDS
ENDED = False

# FONT SIZES
font10 = QtGui.QFont('Helvetica',10)
font12 = QtGui.QFont('Helvetica',12)
font14 = QtGui.QFont('Helvetica',14)
font16 = QtGui.QFont('Helvetica',16)
font18 = QtGui.QFont('Helvetica',18)
font20 = QtGui.QFont('Helvetica',20)
font30 = QtGui.QFont('Helvetica',30, QtGui.QFont.Bold)
font48 = QtGui.QFont('Helvetica',48)

# BUTTONS
h1 = 17
d1 = 27
s1 = 22
e1 = 23

hb = bjb.HWButton(h1)
sb = bjb.HWButton(s1)
db = bjb.HWButton(d1)
eb = bjb.HWButton(e1)

# BUTTON COUNTER TO KEEP TRACK OF STATE MACHINE
button_counter = 0

# INITIAL SETTINGS
number_of_players = "0"
initial_amount = 0
game_mode = ""
user_input = ""
increment_value = 100

# GLOBAL QUEUES USED FOR MULTIPROCESSING INTERACTION
gui_to_bj_queue = mp.Queue()    # gui write, blackjack read
bj_to_gui_queue = mp.Queue()    # blackjack write, gui read

# GAME PROCESS IS CREATED, CHILD PROCESS TO BLACKJACK ALGORITHM IS FORKED
game_process = mp.Process(target=blackjack.blackjack_process, args=(gui_to_bj_queue, bj_to_gui_queue))


###################################################################
###################################################################
########                                                 ##########
########               MAIN WINDOW CLASS                 ##########
########                                                 ##########
########     This class creates/displays the first       ##########
########      GUI ("JACKBLACK" window) and allows        ##########
########      access to the next GUI ("SETTINGS").       ##########
########                                                 ##########
###################################################################
###################################################################

class Ui_MainWindow(QtCore.QObject):

    def __init__(self):
        super().__init__()

#########################################
        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        #self.timer.timeout.connect(sb.check)
        #self.timer.timeout.connect(db.check)
        #self.timer.timeout.connect(eb.check)

        # just start one timer??
        self.timer.start()

        # testing the hw_buttons here
        hb.button_press.connect(lambda: self.mainToSettings(MainWindow))
        #sb.button_press.connect(lambda: self.mainToSettings(MainWindow))
        #db.button_press.connect(lambda: self.mainToSettings(MainWindow))
        #eb.button_press.connect(lambda: self.mainToSettings(MainWindow))
##########################################

    # SWITCH FROM MAIN WINDOW TO SETTINGS WINDOW
    def mainToSettings(self, current_w):
        global button_counter
        self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION

        temp_w = current_w
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        temp_w.hide()

    # STYLES/SETUP OF MAIN GUI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # push button styling/actions
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.mainToSettings(MainWindow))
        self.pushButton.setGeometry(240, 300, 310, 50)
        self.pushButton.setFont(font18)
        self.pushButton.setObjectName("pushButton")

        # JackBlack label styling
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(220, 200, 360, 70)
        self.label.setFont(font30)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        # autogenerated styling
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start Game"))
        self.label.setText(_translate("MainWindow", "JACKBLACK"))


###################################################################
###################################################################
########                                                 ##########
########             SETTINGS WINDOW CLASS               ##########
########                                                 ##########
########        This class creates the settings          ##########
########       GUI ("SETTINGS" window) and allows        ##########
########     access to the next GUI ("CONFIRM BOX").     ##########
########                                                 ##########
###################################################################
###################################################################

class Ui_SettingsWindow(QtCore.QObject):

    def __init__(self):
        super().__init__()
#########################################
        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(sb.check)
        self.timer.timeout.connect(db.check)
        #self.timer.timeout.connect(eb.check)

        # just start one timer
        self.timer.start()

        # testing the hw_buttons here
        hb.button_press.connect(self.decrementNumPlayer)
        sb.button_press.connect(self.continueNumPlayer)
        db.button_press.connect(self.incrementNumPlayer)
        #eb.button_press.connect(lambda: self.mainToSettings(MainWindow))
##########################################

    # adding increment, decrement, continue NumPlayer functions
    def incrementNumPlayer(self):
        index = self.numberOfPlayersComboBox.currentIndex()
        if index < 4:
            self.numberOfPlayersComboBox.setCurrentIndex(index+1)

    def decrementNumPlayer(self):
        index = self.numberOfPlayersComboBox.currentIndex()
        if index > 0:
            self.numberOfPlayersComboBox.setCurrentIndex(index-1)

    def continueNumPlayer(self):
        global button_counter
        #self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.initialAmountSetting()


    # adding functions to buttons for initial amount
    def initialAmountSetting(self):
        # testing the hw_buttons here
        hb.button_press.connect(self.decrementAmount)
        sb.button_press.connect(self.continueAmount)
        db.button_press.connect(self.incrementAmount) 

    def incrementAmount(self):
        global increment_value
        amount = self.startingAmountSpinBox.value()
        #amount = amount + initial_amount
        self.startingAmountSpinBox.setValue(amount+increment_value)

    def decrementAmount(self):
        global increment_value
        amount = self.startingAmountSpinBox.value()
        self.startingAmountSpinBox.setValue(amount-increment_value)

    def continueAmount(self):
        global button_counter
        #self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.gameModeSetting()        


    def gameModeSetting(self):
        # testing the hw_buttons here
        hb.button_press.connect(self.decrementGameMode)
        sb.button_press.connect(self.continueGameMode)
        db.button_press.connect(self.incrementGameMode)    

    # adding functions to buttons for Game Mode
    def incrementGameMode(self):
        index = self.gameModeSelect1ComboBox.currentIndex()
        if index < 4:
            self.gameModeSelect1ComboBox.setCurrentIndex(index+1)        

    def decrementGameMode(self):
        index = self.gameModeSelect1ComboBox.currentIndex()
        if index > 0:
            self.gameModeSelect1ComboBox.setCurrentIndex(index-1)

    def continueGameMode(self):
        global button_counter
        #self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.userInputSetting()

    def userInputSetting(self):
        # testing the hw_buttons here
        hb.button_press.connect(self.decrementUI)
        sb.button_press.connect(self.continueUI)
        db.button_press.connect(self.incrementUI)    

    def incrementUI(self):
        global increment_value
        amount = self.insert.value()
        #amount = amount + initial_amount
        self.insert.setValue(amount+increment_value)

    def decrementUI(self):
        global increment_value
        amount = self.insert.value()
        #amount = amount + initial_amount
        self.insert.setValue(amount-increment_value)

    def continueUI(self):
        global button_counter
        #self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.openWindow(self.SettingsWindow)  
        #self.pushButton.setEnabled(True) # turning push button on               

    # SETTINGS OPTIONS/OPEN CONFIRM BOX
    def openWindow(self, settings_w):
        # storing input values for the settings
        # testing the hw_buttons here

        number_of_players = self.numberOfPlayersComboBox.currentText()
        initial_amount = self.startingAmountSpinBox.value()
        game_mode = self.gameModeSelect1ComboBox.currentText()
        user_input = self.insert.value()

        #user_input = self.insert.value()

        # opening up the confirmation box with user-selected settings
        self.window = QtWidgets.QDialog()
        self.ui = Ui_confirm_dialogbox(number_of_players, initial_amount, game_mode, user_input)
        self.ui.setupUi(self, self.window, settings_w)

        # displaying the values onto confirmation box
        self.ui.confirm_list_widget.addItems(["Number of Players: " + number_of_players,
            "Starting Amount: " + str(initial_amount),
            "Game Mode: " + str(game_mode),
            "User Input: " + str(user_input)])
        self.window.show()

    def gameModeChanged(self, game_mode):
        if game_mode == "Winning Amount":
            self.insert = QtWidgets.QSpinBox(self.formLayoutWidget,
            maximum=5000,
            minimum=0,
            value=1000,
            singleStep=100)
        elif game_mode == "Number of Wins":
            self.insert = QtWidgets.QSpinBox(self.formLayoutWidget,
            maximum=50,
            minimum=0,
            value=10,
            singleStep=1)
        elif game_mode == "Total Games":
            self.insert = QtWidgets.QSpinBox(self.formLayoutWidget,
            maximum=50,
            minimum=0,
            value=10,
            singleStep=1)
        elif game_mode == "Duration":
            self.insert = QtWidgets.QSpinBox(self.formLayoutWidget,
            maximum=300,
            minimum=0,
            value=60,
            singleStep=5)
        else:
            pass


    # STYLES/SETUP OF SETTINGS GUI
    def setupUi(self, SettingsWindow):
        self.SettingsWindow = SettingsWindow
        self.SettingsWindow.setObjectName("SettingsWindow")
        self.SettingsWindow.resize(WIDTH, HEIGHT)
        self.SettingsWindow.setFont(font12)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")

        # game play settings label styling
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(300, 50, 360, 70)
        self.label.setFont(font14)
        self.label.setObjectName("label")

        # creating form layout of widgets
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(180, 130, 500, 200)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        # creating/styling numPlayers widget
        self.numberOfPlayersLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.numberOfPlayersLabel.setObjectName("numberOfPlayersLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.numberOfPlayersLabel)
        self.numberOfPlayersComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.numberOfPlayersComboBox.setObjectName("numberOfPlayersComboBox")
        self.numberOfPlayersComboBox.addItem("")
        self.numberOfPlayersComboBox.addItem("")
        self.numberOfPlayersComboBox.addItem("")
        self.numberOfPlayersComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.numberOfPlayersComboBox)
        
        # creating/styling startingAmount widget
        self.startingAmountLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.startingAmountLabel.setObjectName("startingAmountLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.startingAmountLabel)
        self.startingAmountSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget,
            maximum=5000,
            minimum=0,
            value=1000,
            singleStep=100)
        self.startingAmountSpinBox.setObjectName("startingAmountSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.startingAmountSpinBox)
        
        # creating/styling gameMode widget
        self.gameModeSelect1Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.gameModeSelect1Label.setObjectName("gameModeSelect1Label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.gameModeSelect1Label)
        self.gameModeSelect1ComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.gameModeSelect1ComboBox.addItems(["Winning Amount", "Number of Wins", "Total Games", "Duration"])
        self.gameModeSelect1ComboBox.setObjectName("gameModeSelect1ComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gameModeSelect1ComboBox)
        
        # creating/styling userInput widget
        self.insertLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.insertLabel.setObjectName("insertLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.insertLabel)

        # change the user input field depending on game mode selection
        game_mode = self.gameModeSelect1ComboBox.currentText()
        self.insert = QtWidgets.QSpinBox(self.formLayoutWidget,
            maximum=5000,
            minimum=0,
            value=1000,
            singleStep=100)
        #self.insert = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.insert.setObjectName("insert")
        #self.gameModeSelect1ComboBox.currentTextChanged.connect(self.gameModeChanged)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.insert)
        
        # push button styling
        self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget, clicked=lambda: self.openWindow(self.SettingsWindow))
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pushButton)
        
        # autogenerated styling (may be able to remove?)
        self.SettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.SettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 38))
        self.menubar.setObjectName("menubar")
        self.SettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.SettingsWindow)
        self.statusbar.setObjectName("statusbar")
        self.SettingsWindow.setStatusBar(self.statusbar)
        self.retranslateUi(self.SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(self.SettingsWindow)

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        self.SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
        self.label.setText(_translate("SettingsWindow", "Game Play Settings"))
        self.numberOfPlayersLabel.setText(_translate("SettingsWindow", "Number of Players:"))
        self.numberOfPlayersComboBox.setItemText(0, _translate("SettingsWindow", "1"))
        self.numberOfPlayersComboBox.setItemText(1, _translate("SettingsWindow", "2"))
        self.numberOfPlayersComboBox.setItemText(2, _translate("SettingsWindow", "3"))
        self.numberOfPlayersComboBox.setItemText(3, _translate("SettingsWindow", "4"))
        self.startingAmountLabel.setText(_translate("SettingsWindow", "Starting Amount:"))
        self.gameModeSelect1Label.setText(_translate("SettingsWindow", "Game Mode:"))
        self.insertLabel.setText(_translate("SettingsWindow", "User Input:"))
        self.pushButton.setText(_translate("SettingsWindow", "CONTINUE"))


###################################################################
###################################################################
########                                                 ##########
########                CONFIRM BOX CLASS                ##########
########                                                 ##########
########      This class creates the Confirm Box         ##########
########     GUI ("CONFIRM BOX" window) and allows       ##########
########    access to the next GUI ("PLAYER READY").     ##########
########                                                 ##########
###################################################################
###################################################################

class Ui_confirm_dialogbox(QtCore.QObject):

    # INITIALIZING THE GAME SETTINGS FROM PREVIOUS GUI
    def __init__(self, number_of_players, initial_amount, game_mode, user_input):
        super().__init__()

        self.number_of_players = number_of_players
        self.initial_amount = initial_amount
        self.game_mode = game_mode
        self.user_input = user_input
    

    def previousButtonSettings(self):
        # testing the hw_buttons here
        hb.button_press.connect(self.decrementUI)
        sb.button_press.connect(self.continueUI)
        db.button_press.connect(self.incrementUI)         

    # UPON CONFIRM BUTTON PRESS: CLOSE CURRENT GUIS, OPEN PLAYER_READY GUI
    def confirm_connection(self, set_w):
        # need to open new window and hide settings window
        set_w.hide()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Player_ReadyWindow(self.number_of_players, self.initial_amount, self.game_mode, self.user_input)
        self.ui.setupUi(self.window)
        self.window.show()

        self.continueConfirmation()

    # UPON CANCEL BUTTON PRESS: RESET BUTTON CONNECTIONS
    def reject_connection(self, prev_w):
        hb.button_press.disconnect() # TESTING DISCONNECTION
        db.button_press.disconnect()

        # testing the hw_buttons here
        hb.button_press.connect(prev_w.decrementNumPlayer)
        sb.button_press.connect(prev_w.continueNumPlayer)
        db.button_press.connect(prev_w.incrementNumPlayer)




    def continueConfirmation(self):
        global button_counter
        #self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        db.button_press.disconnect()


    # STYLES/SETUP OF CONFIRM BOX GUI
    def setupUi(self, ui_settings_self, confirm_dialogbox, SettingsWindow):
        prevSettings = ui_settings_self
        self.SettingsWindow = SettingsWindow
        confirm_dialogbox.setObjectName("confirm_dialogbox")
        confirm_dialogbox.resize(WIDTH, HEIGHT)

        # button styles/configurations
        self.buttonBox = QtWidgets.QDialogButtonBox(confirm_dialogbox)
        self.buttonBox.setGeometry(180, 260, 500, 200)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.confirm_connection(SettingsWindow))
        self.buttonBox.rejected.connect(lambda: self.reject_connection(prevSettings))
        hb.button_press.connect(self.buttonBox.accepted) # hb = hit button
        db.button_press.connect(self.buttonBox.rejected) # db = double button

        # confirm box geometry/layout
        self.widget = QtWidgets.QWidget(confirm_dialogbox)
        self.widget.setGeometry(180, 100, 500, 200)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # confirmation label text styles/layout
        self.confirm_label = QtWidgets.QLabel(self.widget)
        self.confirm_label.setFont(font10)
        self.confirm_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.confirm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.confirm_label.setObjectName("confirm_label")
        self.verticalLayout.addWidget(self.confirm_label)
        self.confirm_list_widget = QtWidgets.QListWidget(self.widget)
        self.confirm_list_widget.setObjectName("confirm_list_widget")
        self.verticalLayout.addWidget(self.confirm_list_widget)

        # autogenerated styling
        self.retranslateUi(confirm_dialogbox)
        self.buttonBox.accepted.connect(confirm_dialogbox.accept)
        self.buttonBox.rejected.connect(confirm_dialogbox.reject)
        QtCore.QMetaObject.connectSlotsByName(confirm_dialogbox)

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, confirm_dialogbox):
        _translate = QtCore.QCoreApplication.translate
        confirm_dialogbox.setWindowTitle(_translate("confirm_dialogbox", "Confirmation"))
        self.confirm_label.setText(_translate("confirm_dialogbox", "Are these configurations correct?"))


###################################################################
###################################################################
########                                                 ##########
########               PLAYER READY CLASS                ##########
########                                                 ##########
########      This class creates the Player Ready        ##########
########     GUI ("PLAYER READY" window) and allows      ##########
########    access to the next GUI ("PLAYER GAME").      ##########
########     This contains the game_process, which       ##########
########      starts the official blackjack game.        ##########
########                                                 ##########
###################################################################
###################################################################

class Ui_Player_ReadyWindow(QtCore.QObject):

    # INITIALIZES GAMEPLAY SETTINGS FROM PRIOR GUI
    def __init__(self, numPlayers, startingAmount, gameMode, userInput):
        super().__init__()

        self.numPlayers = numPlayers
        self.startingAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput
        self.player_cards = []
        self.bet = 0
        # testing the hw_buttons here
        #hb.button_press.connect(self.readyForGame)

    # UPON BET_IT BUTTON PRESS: CLEAR ALL WIDGETS ON THE SCREEN, STORE DESIRED BET FOR GAME
    def bet_it(self, p1_mw):
        global button_counter
        button_counter += 1 # changing state
        hb.button_press.disconnect()
        self.bettingButtons()

        # clearing all widgets (necessary to avoid errors)
        for i in reversed(range(self.formLayout.count())): 
            self.formLayout.itemAt(i).widget().setParent(None)

        # TODO: need to change this to be similar to below formatting (get rid of centralwidget, need formLayout)
        # set vertical box layout
        #self.centralwidget.setLayout(QtWidgets.QVBoxLayout())
        #self.betting_label = QtWidgets.QLabel("Betting for this round?")

        # bet label styles/layout
        self.betting_label = QtWidgets.QLabel(self.centralwidget)
        self.betting_label.setText("Betting for this round?")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.betting_label)
        self.betting_label.setGeometry(180, 100, 500, 200)
        self.betting_label.setFont(font16)
        self.betting_label.setAcceptDrops(False)
        self.betting_label.setAlignment(QtCore.Qt.AlignCenter)
        self.betting_label.setObjectName("betting_label")

        
        # betting amount scroll bar
        self.scroll_bet = QtWidgets.QSpinBox(self.centralwidget,
            maximum=500,
            minimum=10,
            value=10,
            singleStep=10)
        self.scroll_bet.setGeometry(400, 100, 500, 200)
        self.scroll_bet.setFont(font16)
        self.scroll_bet.setObjectName("scroll_bet")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.scroll_bet)
             
        # ok button styles/layout
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openWindow(p1_mw))
        self.ok_pushButton.setText("OK")
        self.ok_pushButton.setGeometry(180, 170, 500, 200)
        self.ready_pushButton.setFont(font16)
        self.ready_pushButton.setObjectName("ok_pushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ok_pushButton)

    def bettingButtons(self):
        hb.button_press.connect(self.decrementBet)
        db.button_press.connect(self.incrementBet)
        sb.button_press.connect(self.continueBet)
        sb.button_press.connect(self.ok_pushButton.accepted)

############################
    def incrementBet(self):
        global increment_value
        amount = self.scroll_bet.value()
        #amount = amount + initial_amount
        self.scroll_bet.setValue(amount+increment_value)

    def decrementBet(self):
        global increment_value
        amount = self.scroll.value()
        self.scroll_bet.setValue(amount-increment_value)

    def continueBet(self):
        global button_counter
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
#############################

    # START BLACKJACK GAME; OPEN GAME WINDOW
    def openWindow(self, main_w):
        # start official Blackjack game
        self.startBlackJack() 

        # checking IDs in message queue/grabbing message contents (player cards)
        # this needs to account for multiple rounds
        while(1):
            msg = bj_to_gui_queue.get()
            if msg.id == "player_cards":
                self.player_cards = msg.content
                break
            elif msg.id == "dealer_cards":
                self.dealer_cards = msg.content
            else:
                pass

        # open new game window
        temp_w = main_w
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GameWindow(self.numPlayers, self.startingAmount, self.gameMode, self.userInput, self.bet, self.player_cards)
        self.ui.setupUi(self.window)
        self.window.show()

        # displaying the betting amount
        self.bet = self.scroll_bet.value()
        #self.bet = int(self.user_bet.text())
        self.ui.current_bet_field.setPlainText(str(self.bet))
        self.ui.your_cards_left_field.setPlainText(str(self.player_cards[0]))
        self.ui.your_cards_right_field.setPlainText(str(self.player_cards[1]))
        #self.ui.dealer_left_field.setPlainText(str(self.dealer_cards[0]))
        #self.ui.dealer_right_field.setPlainText(str(self.dealer_cards[1]))

        # close current betting window
        temp_w.hide()

    # OFFICIALLY STARTS BLACKJACK GAME; GAME_PROCESS STARTED
    def startBlackJack(self):
        # game_process is started here
        # need to make this into loop?
        # initialize variables
        game_process.start()

        # saving bet data from previous input
        self.bet = self.scroll_bet.value()
        #self.bet = int(self.user_bet.text())

        # creating/putting message to queue
        start_msg = Message("game_start", [self.numPlayers, self.startingAmount, self.bet, self.gameMode, self.userInput])
        gui_to_bj_queue.put(start_msg)

        # printing game_process pid (for debugging/killing process)
        game_process_pid = game_process.pid
        print("Game pid: ", game_process_pid)

    # STYLES/SETUP OF PLAYER_READY GUI
    def setupUi(self, Player_ReadyWindow):
        Player_ReadyWindow.setObjectName("Player_ReadyWindow")
        Player_ReadyWindow.resize(WIDTH, HEIGHT)
        self.centralwidget = QtWidgets.QWidget(Player_ReadyWindow)
        self.centralwidget.setObjectName("centralwidget")

        # making a form layout
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(150, 130, 500, 200)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        # player label styling
        self.player_label = QtWidgets.QLabel(self.centralwidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.player_label)
        self.player_label.setFont(font48)
        self.player_label.setAcceptDrops(False)
        self.player_label.setAlignment(QtCore.Qt.AlignCenter)
        self.player_label.setObjectName("player_label")

        # ready_push button styling/layout
        self.ready_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.bet_it(Player_ReadyWindow))
        self.ready_pushButton.setGeometry(100, 160, 250, 61)
        self.ready_pushButton.setFont(font12)
        self.ready_pushButton.setObjectName("ready_pushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ready_pushButton)
        
        hb.button_press.connect(self.ready_pushButton.clicked)

        # autogenerated styling (might be able to remove?)
        Player_ReadyWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Player_ReadyWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 610, 22))
        self.menubar.setObjectName("menubar")
        Player_ReadyWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Player_ReadyWindow)
        self.statusbar.setObjectName("statusbar")
        Player_ReadyWindow.setStatusBar(self.statusbar)
        self.retranslateUi(Player_ReadyWindow)
        QtCore.QMetaObject.connectSlotsByName(Player_ReadyWindow)

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, Player_ReadyWindow):
        _translate = QtCore.QCoreApplication.translate
        Player_ReadyWindow.setWindowTitle(_translate("Player_ReadyWindow", "Player 1"))
        self.player_label.setText(_translate("Player_ReadyWindow", "Player 1"))
        self.ready_pushButton.setText(_translate("Player_ReadyWindow", "PRESS HERE WHEN READY!"))


###################################################################
###################################################################
########                                                 ##########
########                NEXT ROUND CLASS                 ##########
########                                                 ##########
########      This class creates the NEXT ROUND          ##########
########     GUI and allows access to next round.        ##########
########                                                 ##########
###################################################################
###################################################################


class Ui_confirm_round(QtCore.QObject):

    def __init__(self):
        super().__init__()
    
    # UPON CONFIRM BUTTON PRESS: CLOSE CURRENT GUIS, OPEN PLAYER_READY GUI
    def confirm_connection(self):
        pass

    # UPON CANCEL BUTTON PRESS: DO NOTHING
    def reject_connection(self):
        pass

    # STYLES/SETUP OF CONFIRM BOX GUI
    def setupUi(self, confirm_round):
        confirm_round.setObjectName("confirm_round")
        confirm_round.resize(WIDTH, HEIGHT)

        # button styles/configurations
        self.buttonBox = QtWidgets.QDialogButtonBox(confirm_round)
        self.buttonBox.setGeometry(180, 260, 500, 200)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.confirm_connection())
        self.buttonBox.rejected.connect(lambda: self.reject_connection())

        # confirm box geometry/layout
        self.widget = QtWidgets.QWidget(confirm_round)
        self.widget.setGeometry(180, 100, 500, 200)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # confirmation label text styles/layout
        self.confirm_label = QtWidgets.QLabel(self.widget)
        self.confirm_label.setFont(font10)
        self.confirm_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.confirm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.confirm_label.setObjectName("confirm_label")
        self.verticalLayout.addWidget(self.confirm_label)
        self.confirm_list_widget = QtWidgets.QListWidget(self.widget)
        self.confirm_list_widget.setObjectName("confirm_list_widget")
        self.verticalLayout.addWidget(self.confirm_list_widget)

        # autogenerated styling
        self.retranslateUi(confirm_round)
        self.buttonBox.accepted.connect(confirm_round.accept)
        self.buttonBox.rejected.connect(confirm_round.reject)
        QtCore.QMetaObject.connectSlotsByName(confirm_round)

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, confirm_round):
        _translate = QtCore.QCoreApplication.translate
        confirm_round.setWindowTitle(_translate("confirm_round", "Confirmation"))
        self.confirm_label.setText(_translate("confirm_round", "READY FOR NEXT ROUND?"))


###################################################################
###################################################################
########                                                 ##########
########                  END GAME CLASS                 ##########
########                                                 ##########
########      This class creates the NEXT ROUND          ##########
########     GUI and allows access to next round.        ##########
########                                                 ##########
###################################################################
###################################################################


class Ui_end_game(QtCore.QObject):
    def __init__(self):
        super().__init__()

    # UPON CONFIRM BUTTON PRESS: CLOSE CURRENT GUIS, OPEN PLAYER_READY GUI
    def play_again_connection(self, game_w):
        game_w.hide()
        result = "game_process" in globals()
        if result:
            game_process.terminate()
            game_process.join()
            #sys.exit(app.quit())

        else:
            pass
        # testing this
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    # UPON CANCEL BUTTON PRESS: DO NOTHING
    def end_game_connection(self):
        result = "game_process" in globals()
        if result:
            game_process.terminate()
            game_process.join()
            # this will close the application, but prints out an event loop running error
            sys.exit(app.exec_())
        else:
            pass

    # STYLES/SETUP OF CONFIRM BOX GUI
    def setupUi(self, end_game, Ui_GameWindow):
        end_game.setObjectName("end_game")
        end_game.resize(WIDTH, HEIGHT)

        # button styles/configurations
        self.buttonBox = QtWidgets.QDialogButtonBox(end_game)
        self.buttonBox.setGeometry(180, 260, 500, 200)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.play_again_connection(Ui_GameWindow))
        self.buttonBox.rejected.connect(lambda: self.end_game_connection())

        # confirm box geometry/layout
        self.widget = QtWidgets.QWidget(end_game)
        self.widget.setGeometry(180, 100, 500, 200)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # confirmation label text styles/layout
        self.confirm_label = QtWidgets.QLabel(self.widget)
        self.confirm_label.setFont(font10)
        self.confirm_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.confirm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.confirm_label.setObjectName("confirm_label")
        self.verticalLayout.addWidget(self.confirm_label)
        self.confirm_list_widget = QtWidgets.QListWidget(self.widget)
        self.confirm_list_widget.setObjectName("confirm_list_widget")
        self.verticalLayout.addWidget(self.confirm_list_widget)

        # autogenerated styling
        self.retranslateUi(end_game)
        self.buttonBox.accepted.connect(end_game.accept)
        self.buttonBox.rejected.connect(end_game.reject)
        QtCore.QMetaObject.connectSlotsByName(end_game)

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, end_game):
        _translate = QtCore.QCoreApplication.translate
        end_game.setWindowTitle(_translate("end_game", "Confirmation"))
        self.confirm_label.setText(_translate("end_game", "GAME END"))


###################################################################
###################################################################
########                                                 ##########
########                PLAYER GAME CLASS                ##########
########                                                 ##########
########      This class creates the Player Game         ##########
########     GUI ("PLAYER GAME" window) and allows       ##########
########    for full gameplay experience. Majority       ##########
########     of game mode checks and functionality       ##########
########             of GUI is located here.             ##########
########                                                 ##########
###################################################################
###################################################################

class Ui_GameWindow(QtCore.QObject):

    # INITIALIZING GAME SETTINGS FROM PRIOR WINDOW
    def __init__(self, numPlayers, startingAmount, gameMode, userInput, bet, playerCards):
        super().__init__()

        self.numPlayers = numPlayers
        self.currentAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput
        self.bet = bet
        self.player_cards = playerCards
        self.double_button_clicked = False
        #self.timer = qtc.QTimer(interval=50, timeout=self.check)
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(sb.check)
        self.timer.timeout.connect(db.check)
        self.timer.timeout.connect(eb.check)

        # just start one timer??
        self.timer.start()


        # testing the hw_buttons here
        hb.button_press.connect(self.hit_it)
        sb.button_press.connect(self.stand_it)
        db.button_press.connect(self.double_it)
        eb.button_press.connect(self.exit_it)        

    
    def open_next_round(self, d_cards, p_cards, scoring, wallets, bust, bj):
        # opening up the next round screen
        self.window = QtWidgets.QDialog()
        self.ui = Ui_confirm_round()
        self.ui.setupUi(self.window)
        self.window.show()

        if bust:
            self.ui.confirm_list_widget.addItems(["Dealer Cards: " + str(d_cards),
            "Player Cards: " + str(p_cards),
            "Round Score: " + str(scoring), "Current Wallets: " + str(wallets),
            "PLAYER BUST!"])
        elif bj:
            self.ui.confirm_list_widget.addItems(["Dealer Cards: " + str(d_cards),
            "Player Cards: " + str(p_cards),
            "Round Score: " + str(scoring), "Current Wallets: " + str(wallets),
            "PLAYER BLACKJACK!"])
        else:
            # displaying the values onto confirmation box
            self.ui.confirm_list_widget.addItems(["Dealer Cards: " + str(d_cards),
            "Player Cards: " + str(p_cards),
            "Round Score: " + str(scoring), "Current Wallets: " + str(wallets)])
    
    def done_round(self):
        while(1):
            msg0 = bj_to_gui_queue.get()

            if msg0.id == "player_cards":
                self.player_cards = msg0.content
                self.your_cards_left_field.setPlainText(str(self.player_cards[0]))
                self.your_cards_right_field.setPlainText(str(self.player_cards[1]))
                # reset the gui bet and starting amount here
                self.amount_left_label.setText("Amount Left: " + str(self.currentAmount))
                self.current_bet_field.setPlainText(str(self.bet))
            elif msg0.id == "dealer_cards":
                self.dealer_cards = msg0.content
                #self.dealer_left_field.setPlainText(str(self.dealer_cards[0]))
                #self.dealer_right_field.setPlainText(str(self.dealer_cards[1]))
                break
            elif msg0.id == "GAME OVER!":
                # end the game
                #self.exit_it() # TESTING (THIS WORKED!!)
                # instead of exiting, have a screen pop up with "WINNER!" or "YOU LOST!"
                wins = msg0.content[0]
                game_result = msg0.content[1]
                temp_w = self.window
                self.window = QtWidgets.QDialog()
                self.ui = Ui_end_game() # (player, num_wins, if player won)
                self.ui.setupUi(self.window, temp_w)
                self.window.show()


                if game_result:
                    winner = "YOU WON!"
                else:
                    winner = "YOU LOST!"

                self.ui.confirm_list_widget.addItems(["Number of Wins: " + str(wins),
                    "Results: " + winner])

                break
            else:
                pass

    # UPON DOUBLE BUTTON PRESSED; UPDATE BET VALUE
    # FIX END ROUND PART
    def double_it(self):
        self.double_button_clicked = True

        if self.double_button_clicked:
            msg = Message("double", self.bet)
            gui_to_bj_queue.put(msg)

            while(1):
                msg1 = bj_to_gui_queue.get()
                if msg1.id == "player_cards":
                    self.player_cards = msg1.content
                    self.your_cards_left_field.setPlainText(str(self.player_cards))
                    self.your_cards_right_field.setPlainText(str(""))
                elif msg1.id == "wallet":
                    self.currentAmount = msg1.content
                    self.amount_left_label.setText("Amount Left: " + str(self.currentAmount))
                elif msg1.id == "doubled":
                    value = msg1.content
                    #self.bet = value
                    self.current_bet_field.setPlainText(str(value))
                elif msg1.id == "done_round":
                    # need to go back and reset DOUBLE/STAND/HIT BUTTON functionality
                    self.double_button_clicked == False
                    
                    p1_cards = msg1.content[1]
                    d_cards = msg1.content[0]
                    scoring = msg1.content[2]
                    wallets = msg1.content[3]
                    bust = msg1.content[4]
                    bj = msg1.content[5]
                    

                    # self.bet = bet (reset?)
                    # adding time delay before going to next screen
                    QtTest.QTest.qWait(DELAYED)
                    # put in the player and dealer cards to display in next round screen
                    self.open_next_round(d_cards, p1_cards, scoring, wallets, bust, bj)
                    QtTest.QTest.qWait(DELAYED)
                    self.done_round()
                    break
                else:
                    pass
        else:
            pass
        

        #self.double_button_clicked = True

    # TODO
    # when "STAND" button is pressed, do nothing to current bet, do nothing to cards, reveal dealer cards
    def stand_it(self):
        # not being incremented properly for the total amount here
        msg = Message("stand", None)
        gui_to_bj_queue.put(msg)
        self.dealer_cards = []

        while(1):
            msg = bj_to_gui_queue.get()
            if msg.id == "dealer_cards":
                self.dealer_cards = msg.content
            elif msg.id == "wallet":
                self.currentAmount = msg.content
                self.amount_left_label.setText("Amount Left: " + str(self.currentAmount))
            elif msg.id == "done_round":
                
                p1_cards = msg.content[1]
                d_cards = msg.content[0]
                scoring = msg.content[2]
                wallets = msg.content[3]
                bust = msg.content[4]
                bj = msg.content[5]
                

                # self.bet = bet (reset?)
                # adding time delay before going to next screen?
                QtTest.QTest.qWait(DELAYED)
                # put in the player and dealer cards to display in next round screen
                self.open_next_round(d_cards, p1_cards, scoring, wallets, bust, bj)
                QtTest.QTest.qWait(DELAYED)
                self.done_round()
                break
            else:
                pass
        #self.dealer_left_field.setPlainText(str(self.dealer_cards[0]))
        #self.dealer_right_field.setPlainText(str(self.dealer_cards[1]))

    # TODO
    # when "HIT" button is pressed, do nothing to current bet, add another card to player
    def hit_it(self):
        msg = Message("hit", None)
        gui_to_bj_queue.put(msg)

        while(1):
            msg = bj_to_gui_queue.get()
            if msg.id == "player_cards":
                self.player_cards = msg.content
                self.your_cards_left_field.setPlainText(str(self.player_cards))
                self.your_cards_right_field.setPlainText(str(""))
                break
            elif msg.id == "wallet":
                self.currentAmount = msg.content
                self.amount_left_label.setText("Amount Left: " + str(self.currentAmount))
            elif msg.id == "done_round":
                p1_cards = msg.content[1]
                d_cards = msg.content[0]
                scoring = msg.content[2]
                wallets = msg.content[3]
                bust = msg.content[4]
                bj = msg.content[5]

                if bust:
                    QtTest.QTest.qWait(DELAYED)
                    # put in the player and dealer cards to display in next round screen
                    self.open_next_round(d_cards, p1_cards, scoring, wallets, bust, bj)
                    QtTest.QTest.qWait(DELAYED)
                    self.done_round()
                elif bj:
                    QtTest.QTest.qWait(DELAYED)
                    # put in the player and dealer cards to display in next round screen
                    self.open_next_round(d_cards, p1_cards, scoring, wallets, bust, bj)
                    QtTest.QTest.qWait(DELAYED)
                    self.done_round()
                else:
                    self.done_round()
                break
            else:
                pass
        

    def exit_it(self):
        # TODO: fix this code for exit button
        result = "game_process" in globals()
        if result:
            game_process.terminate()
            game_process.join()
            # this will close the application, but prints out an event loop running error
            sys.exit(app.exec_())
        else:
            pass

    # setting up main window and components
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(250, 280, 300, 150)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.your_cards_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.your_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.your_cards_layout.setObjectName("your_cards_layout")

        self.your_cards_left_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget,
            readOnly=True)
        self.your_cards_left_field.setObjectName("your_cards_left_field")
        self.your_cards_left_field.setFont(font20)
        self.your_cards_layout.addWidget(self.your_cards_left_field)
        self.your_cards_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget,
            readOnly=True)
        self.your_cards_right_field.setObjectName("your_cards_right_field")
        self.your_cards_right_field.setFont(font20)
        self.your_cards_layout.addWidget(self.your_cards_right_field)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(250, 30, 300, 150)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")

        self.dealer_cards_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.dealer_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.dealer_cards_layout.setObjectName("dealer_cards_layout")
        self.dealer_left_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2,
            readOnly=True)
        self.dealer_left_field.setObjectName("dealer_left_field")
        self.dealer_left_field.setFont(font20)
        self.dealer_cards_layout.addWidget(self.dealer_left_field)
        self.dealer_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2,
            readOnly=True)
        self.dealer_right_field.setObjectName("dealer_right_field")
        self.dealer_right_field.setFont(font20)
        self.dealer_cards_layout.addWidget(self.dealer_right_field)

        self.current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget,
            readOnly=True)
        self.current_bet_field.setFont(font20)
        self.current_bet_field.setGeometry(100, 310, 110, 110)
        self.current_bet_field.setObjectName("current_bet_field")

        # creating the amount left label
        self.amount_left_label = QtWidgets.QLabel(self.centralwidget)
        self.amount_left_label.setFont(font10)
        self.amount_left_label.setGeometry(600, 10, 300, 50)
        self.amount_left_label.setObjectName("amount_left_label")
        #self.amount_left_label.setText(str(self.currentAmount))

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(600, 280, 100, 150)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.hit_it())
        self.hit_button.setObjectName("hit_button")
        self.verticalLayout.addWidget(self.hit_button)
        self.double_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.double_it())
        self.double_button.setObjectName("double_button")
        self.verticalLayout.addWidget(self.double_button)
        self.stand_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.stand_it())
        self.stand_button.setObjectName("stand_button")
        self.verticalLayout.addWidget(self.stand_button)
        self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.exit_it())
        self.exit_button.setObjectName("exit_button")
        self.verticalLayout.addWidget(self.exit_button)

        # change font size to be a lot bigger; maybe size 10?
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(355, 200, 110, 110)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(355, 140, 140, 110)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(110, 230, 110, 110)
        self.label_3.setObjectName("label_3")
        self.label.setFont(font10)
        self.label_2.setFont(font10)
        self.label_3.setFont(font10)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.amount_left_label.setText(_translate("MainWindow", "Amount Left: ") + str(self.currentAmount))
        self.hit_button.setText(_translate("MainWindow", "HIT"))
        self.double_button.setText(_translate("MainWindow", "DOUBLE"))
        self.stand_button.setText(_translate("MainWindow", "STAND"))
        self.exit_button.setText(_translate("MainWindow", "EXIT GAME"))
        self.label.setText(_translate("MainWindow", "Your Cards:"))
        self.label_2.setText(_translate("MainWindow", "Dealer\'s Cards:"))
        self.label_3.setText(_translate("MainWindow", "Current Bet:"))


if __name__ == "__main__":
    import sys
    #initGPIO()
    #GPIO.setmode(GPIO.BCM)
    #timer.start()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #self.startBlackJack()
    #  This line will close the app, but I have it above in exit_it() function
    sys.exit(app.exec_())
