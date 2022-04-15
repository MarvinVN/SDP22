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
import blackjack_multi_HW
from blackjack_globals import Message
import multiprocessing as mp
import blackjack_buttons as bjb
from adafruit_pn532.spi import PN532_SPI
from RPi import GPIO
import board
import busio
from digitalio import DigitalInOut
#from time import sleep
from RPi import GPIO

# DIMENSIONS OF TOUCH DISPLAY
HEIGHT = 480
WIDTH = 800

# TIME DELAY (IN MILLISECONDS)
DELAYED = 1500

# GAME ENDS
ENDED = False

# FONT SIZES
font6 = QtGui.QFont('Helvetica',6)
font10 = QtGui.QFont('Helvetica',10)
font12 = QtGui.QFont('Helvetica',12)
font14 = QtGui.QFont('Helvetica',14)
font16 = QtGui.QFont('Helvetica',16)
font18 = QtGui.QFont('Helvetica',18)
font20 = QtGui.QFont('Helvetica',20)
font30 = QtGui.QFont('Helvetica',30, QtGui.QFont.Bold)
font48 = QtGui.QFont('Helvetica',48)

######### BUTTONS ###########
# PLAYER 1
h1 = 17
d1 = 27
s1 = 22
e1 = 23

hb = bjb.HWButton(h1)
sb = bjb.HWButton(s1)
db = bjb.HWButton(d1)
eb = bjb.HWButton(e1)

# PLAYER 2
h2 = 5
d2 = 6
s2 = 13
e2 = 19

hb2 = bjb.HWButton(h2)
db2 = bjb.HWButton(d2)
sb2 = bjb.HWButton(s2)
eb2 = bjb.HWButton(e2)

# PLAYER 3
h3 = 26
d3 = 16
s3 = 20
e3 = 21

hb3 = bjb.HWButton(h3)
db3 = bjb.HWButton(d3)
sb3 = bjb.HWButton(s3)
eb3 = bjb.HWButton(e3)

# PLAYER 4
h4 = 4
d4 = 18
s4 = 24
e4 = 25

hb4 = bjb.HWButton(h4)
db4 = bjb.HWButton(d4)
sb4 = bjb.HWButton(s4)
eb4 = bjb.HWButton(e4)

# these may not be necessary
button_hit_status = [hb.button_press, hb2.button_press, hb3.button_press, hb4.button_press]
button_double_status = [db.button_press, db2.button_press, db3.button_press, db4.button_press]
button_stand_status = [sb.button_press, sb2.button_press, sb3.button_press, sb4.button_press]
button_exit_status = [eb.button_press, eb2.button_press, eb3.button_press, eb4.button_press]

"""
output_pins = [5, 13, 16, 20, 21]
GPIO.setup(output_pins, GPIO.OUT, initial=GPIO.LOW)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

pn532.SAM_configuration()
"""

# BUTTON COUNTER TO KEEP TRACK OF STATE MACHINE
button_counter = 0

# INITIAL SETTINGS
number_of_players = "0"
initial_amount = 0
game_mode = ""
user_input = ""
increment_value = 100
bet_increment = 10

cards = [[],[],[],[],[]]
amounts_list = [0,0,0,0,0]
player_turn = "p1" # always start with p1

# GLOBAL QUEUES USED FOR MULTIPROCESSING INTERACTION
gui_to_bj_queue = mp.Queue()    # gui write, blackjack read
bj_to_gui_queue = mp.Queue()    # blackjack write, gui read

# GAME PROCESS IS CREATED, CHILD PROCESS TO BLACKJACK ALGORITHM IS FORKED
game_process = mp.Process(target=blackjack_multi_HW.blackjack_process, args=(gui_to_bj_queue, bj_to_gui_queue))


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

        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)

        # just start one timer
        self.timer.start()

        # testing the hw_buttons here
        hb.button_press.connect(lambda: self.mainToSettings(MainWindow))

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

        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(sb.check)
        self.timer.timeout.connect(db.check)

        # just start one timer
        self.timer.start()

        # testing the hw_buttons here
        db.button_press.connect(self.decrementNumPlayer)
        hb.button_press.connect(self.continueNumPlayer)
        sb.button_press.connect(self.incrementNumPlayer)

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
        db.button_press.connect(self.decrementAmount)
        hb.button_press.connect(self.continueAmount)
        sb.button_press.connect(self.incrementAmount) 

    def incrementAmount(self):
        global increment_value
        amount = self.startingAmountSpinBox.value()
        self.startingAmountSpinBox.setValue(amount+increment_value)

    def decrementAmount(self):
        global increment_value
        amount = self.startingAmountSpinBox.value()
        self.startingAmountSpinBox.setValue(amount-increment_value)

    def continueAmount(self):
        global button_counter
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.gameModeSetting()        

    def gameModeSetting(self):
        # testing the hw_buttons here
        db.button_press.connect(self.decrementGameMode)
        hb.button_press.connect(self.continueGameMode)
        sb.button_press.connect(self.incrementGameMode)    

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
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.userInputSetting()

    def userInputSetting(self):
        # testing the hw_buttons here
        db.button_press.connect(self.decrementUI)
        hb.button_press.connect(self.continueUI)
        sb.button_press.connect(self.incrementUI)    

    def incrementUI(self):
        global increment_value
        amount = self.insert.value()
        self.insert.setValue(amount+increment_value)

    def decrementUI(self):
        global increment_value
        amount = self.insert.value()
        self.insert.setValue(amount-increment_value)

    def continueUI(self):
        global button_counter
        self.timer.stop() # TESTING STOP TIMER
        button_counter += 1 # changing state
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
        self.openWindow(self.SettingsWindow)  

    # SETTINGS OPTIONS/OPEN CONFIRM BOX
    def openWindow(self, settings_w):
        # storing input values for the settings
        # testing the hw_buttons here

        number_of_players = self.numberOfPlayersComboBox.currentText()
        initial_amount = self.startingAmountSpinBox.value()
        game_mode = self.gameModeSelect1ComboBox.currentText()
        user_input = self.insert.value()

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

    # This function may not have been implemented
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
        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(db.check)

        # just start one timer
        self.timer.start()

    # UPON CONFIRM BUTTON PRESS: CLOSE CURRENT GUIS, OPEN PLAYER_READY GUI
    def confirm_connection(self, set_w):
        self.continueConfirmation()
        # need to open new window and hide settings window
        set_w.hide()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Player_ReadyWindow(self.number_of_players, self.initial_amount, self.game_mode, self.user_input, self.window)
        self.ui.setupUi(self.window)
        self.window.show()

    # UPON CANCEL BUTTON PRESS: RESET BUTTON CONNECTIONS
    def reject_connection(self, prev_w):
        hb.button_press.disconnect() # TESTING DISCONNECTION
        db.button_press.disconnect()

        # testing the hw_buttons here
        db.button_press.connect(prev_w.decrementNumPlayer)
        hb.button_press.connect(prev_w.continueNumPlayer)
        sb.button_press.connect(prev_w.incrementNumPlayer)

    def continueConfirmation(self):
        global button_counter
        self.timer.stop() # TESTING STOP TIMER
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
    def __init__(self, numPlayers, startingAmount, gameMode, userInput, Player_ReadyWindow):
        super().__init__()

        self.numPlayers = numPlayers
        self.startingAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput
        self.bet = 0
        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(sb.check)
        self.timer.timeout.connect(db.check)
        #self.timer.timeout.connect(eb.check)

        # just start one timer
        self.timer.start()
        #self.bettingButtons()
        db.button_press.connect(self.decrementBet)
        sb.button_press.connect(self.incrementBet)
        #hb.button_press.connect(self.bet_it(Player_ReadyWindow))

    # UPON BET_IT BUTTON PRESS: CLEAR ALL WIDGETS ON THE SCREEN, STORE DESIRED BET FOR GAME
    def bet_it(self, p1_mw):
        # TESTING THIS CODE
        self.p1_mw = p1_mw
        global button_counter
        button_counter += 1 # changing state
        #hb.button_press.disconnect()
        #self.bettingButtons()

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
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openWindow(self.p1_mw))
        self.ok_pushButton.setText("OK")
        self.ok_pushButton.setGeometry(180, 170, 500, 200)

        #hb.button_press.connect(lambda: self.decrementBet)
        #db.button_press.connect(lambda: self.incrementBet)
        hb.button_press.connect(lambda: self.openWindow(self.p1_mw))

        self.ready_pushButton.setFont(font16)
        self.ready_pushButton.setObjectName("ok_pushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ok_pushButton)

    def bettingButtons(self):
        #hb.button_press.disconnect()
        db.button_press.connect(self.decrementBet)
        sb.button_press.connect(self.incrementBet)
        #sb.button_press.connect(self.continueBet)

############################
    def incrementBet(self):
        global bet_increment
        amount = self.scroll_bet.value()
        #amount = amount + initial_amount
        self.scroll_bet.setValue(amount+bet_increment)

    def decrementBet(self):
        global bet_increment
        amount = self.scroll_bet.value()
        self.scroll_bet.setValue(amount-bet_increment)

    def continueBet(self):
        global button_counter
        button_counter += 1 # changing state
        self.timer.stop()
        hb.button_press.disconnect() # TESTING DISCONNECTION
        sb.button_press.disconnect()
        db.button_press.disconnect()
#############################

    # START BLACKJACK GAME; OPEN GAME WINDOW
    def openWindow(self, main_w):
        self.continueBet()

        """
        # start official Blackjack game
        self.startBlackJack() 

        # checking IDs in message queue/grabbing message contents (player cards)
        # this needs to account for multiple rounds

        # need to change this and move into game starting class
        while(1):
            msg = bj_to_gui_queue.get()
            if msg.id == "player_cards":
                self.player_cards = msg.content
                break
            elif msg.id == "dealer_cards":
                self.dealer_cards = msg.content
            else:
                pass
        """
        ###### START BLACKJACK PROCESS FORK ######
        self.startBlackJack() 
        # open new game window
        temp_w = main_w
        self.window = QtWidgets.QMainWindow()
        self.bet = self.scroll_bet.value()
        self.ui = Ui_GameWindow(self.numPlayers, self.startingAmount, self.gameMode, self.userInput, self.bet)
        self.ui.setupUi(self.window)
        self.window.show()

        # close current betting window
        temp_w.hide()

    # OFFICIALLY STARTS BLACKJACK GAME; GAME_PROCESS STARTED
    def startBlackJack(self):
        # game_process is started here
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

        counter = -1

        while(1):
            global cards
            if str(counter) == self.numPlayers:
                break

            msg = bj_to_gui_queue.get() # this should be messages for each player playing
            print("Entered while loop:")
            if msg.id == "p0_cards":
                cards[0] = msg.content
                amounts_list[0] = self.startingAmount
                print("cards[0] = " + str(cards[0]))
            elif msg.id == "p1_cards":
                cards[1] = msg.content
                amounts_list[1] = self.startingAmount
                print("cards[1] = " + str(cards[1]))
            elif msg.id == "p2_cards":
                cards[2] = msg.content
                amounts_list[2] = self.startingAmount
                print("cards[2] = " + str(cards[2]))
            elif msg.id == "p3_cards":
                cards[3] = msg.content
                amounts_list[3] = self.startingAmount
            elif msg.id == "p4_cards":
                cards[4] = msg.content
                amounts_list[4] = self.startingAmount
            else:
                pass
            counter += 1
            print("Counter = " + str(counter))
        print("Left the player while loop")

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
        #hb.button_press.connect(lambda: self.bet_it(Player_ReadyWindow))
        #hb_signal = hb.button_press
        #self.ready_pushButton.hb_signal.connect(lambda: self.bet_it(Player_ReadyWindow))

        # just calling the bet function directly
        self.bet_it(Player_ReadyWindow)

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

        #self.Player_ReadyWindow = Player_ReadyWindow
        #hb.button_press.connect(lambda: self.bet_it(self.Player_ReadyWindow))

    # AUTOGENERATED TRANSLATION FROM GUI TO PYTHON
    def retranslateUi(self, Player_ReadyWindow):
        _translate = QtCore.QCoreApplication.translate
        Player_ReadyWindow.setWindowTitle(_translate("Player_ReadyWindow", "Players READY"))
        self.player_label.setText(_translate("Player_ReadyWindow", "Players READY"))
        self.ready_pushButton.setText(_translate("Player_ReadyWindow", "PRESS HERE WHEN READY!"))



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
    def __init__(self, numPlayers, startingAmount, gameMode, userInput, bet):
        super().__init__()
        global cards, player_turn

        self.numPlayers = numPlayers
        self.currentAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput
        self.bet = bet

        self.player_bets = [bet, bet, bet, bet, bet] # initializing each player bets, added index 0 for dealer
        self.double_button_clicked = False

        self.timer = QtCore.QTimer(interval=50)

        # P1
        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(sb.check)
        self.timer.timeout.connect(db.check)
        self.timer.timeout.connect(eb.check)
        hb.button_press.connect(self.hit_it)
        sb.button_press.connect(self.stand_it)
        db.button_press.connect(self.double_it)
        eb.button_press.connect(self.exit_it)
        # just start one timer
        self.timer.start()

    def reset_buttons(self, currentPlayer):
        global cards
        # opening up the next round screen
        self.timer.stop()

        self.timer = QtCore.QTimer(interval=50)

        if str(currentPlayer) == "1":
            hb.button_press.disconnect()
            sb.button_press.disconnect()
            db.button_press.disconnect()
            eb.button_press.disconnect()

            self.timer.timeout.connect(hb2.check)
            self.timer.timeout.connect(sb2.check)
            self.timer.timeout.connect(db2.check)
            self.timer.timeout.connect(eb2.check)
            hb2.button_press.connect(self.hit_it)
            sb2.button_press.connect(self.stand_it)
            db2.button_press.connect(self.double_it)
            eb2.button_press.connect(self.exit_it)

        elif str(currentPlayer) == "2":
            hb2.button_press.disconnect()
            sb2.button_press.disconnect()
            db2.button_press.disconnect()
            eb2.button_press.disconnect()

            self.timer.timeout.connect(hb3.check)
            self.timer.timeout.connect(sb3.check)
            self.timer.timeout.connect(db3.check)
            self.timer.timeout.connect(eb3.check)
            hb3.button_press.connect(self.hit_it)
            sb3.button_press.connect(self.stand_it)
            db3.button_press.connect(self.double_it)
            eb3.button_press.connect(self.exit_it)

        elif str(currentPlayer) == "3":
            hb3.button_press.disconnect()
            sb3.button_press.disconnect()
            db3.button_press.disconnect()
            eb3.button_press.disconnect()

            self.timer.timeout.connect(hb4.check)
            self.timer.timeout.connect(sb4.check)
            self.timer.timeout.connect(db4.check)
            self.timer.timeout.connect(eb4.check)
            hb4.button_press.connect(self.hit_it)
            sb4.button_press.connect(self.stand_it)
            db4.button_press.connect(self.double_it)
            eb4.button_press.connect(self.exit_it)

        elif str(currentPlayer) == "4":
            hb4.button_press.disconnect()
            sb4.button_press.disconnect()
            db4.button_press.disconnect()
            eb4.button_press.disconnect()

            self.timer.timeout.connect(hb.check)
            self.timer.timeout.connect(sb.check)
            self.timer.timeout.connect(db.check)
            self.timer.timeout.connect(eb.check)
            hb.button_press.connect(self.hit_it)
            sb.button_press.connect(self.stand_it)
            db.button_press.connect(self.double_it)
            eb.button_press.connect(self.exit_it)

        self.timer.start()


    
    def open_next_round(self, scoring, wallets):
        global cards

        # opening up the next round screen
        self.timer.stop()
        hb4.button_press.disconnect()
        sb4.button_press.disconnect()
        db4.button_press.disconnect()
        eb4.button_press.disconnect()
        
        #self.reset_buttons()

        self.window = QtWidgets.QDialog()
        self.ui = Ui_confirm_round()
        self.ui.setupUi(self, self.window)
        self.window.show()

        # displaying the values onto confirmation box
        self.ui.confirm_list_widget.addItem("Dealer Cards: " + str(cards[0]))
        for x in range(1, int(self.numPlayers)+1): # why +1?
            self.ui.confirm_list_widget.addItem("P" + str(x) + " Cards: " + str(cards[x]))
        self.ui.confirm_list_widget.addItems(["Round Score: " + str(scoring), "Current Wallets: " + str(wallets)])
        print("finished displaying end of round...")

    def done_round(self):
        global amounts_list
        
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(sb.check)
        self.timer.timeout.connect(db.check)
        self.timer.timeout.connect(eb.check)

        # just start one timer??
        self.timer.start()

        hb.button_press.connect(self.hit_it)
        sb.button_press.connect(self.stand_it)
        db.button_press.connect(self.double_it)
        eb.button_press.connect(self.exit_it)
        

        while(1):
            msg0 = bj_to_gui_queue.get()
            print("New game message: ", msg0.id, msg0.content)

            if msg0.id == "p0_cards":
                cards[0] = msg0.content
                # no need to display dealer cards, but they must be stored
            elif msg0.id == "p1_cards":
                cards[1] = msg0.content
                print("entered: ", msg0.id, msg0.content)
                self.your_cards_left_field.setPlainText(str(cards[1][0]))
                self.your_cards_right_field.setPlainText(str(cards[1][1]))
                self.amount_left_label.setText("Amount Left: " + str(amounts_list[1]))
                self.current_bet_field.setPlainText(str(self.player_bets[1]))
            elif msg0.id == "p2_cards":
                cards[2] = msg0.content
                print("entered: ", msg0.id, msg0.content)
                self.p2_left_field.setPlainText(str(cards[2][0]))
                self.p2_right_field.setPlainText(str(cards[2][1]))
                self.p2_amount_left_label.setText("Amount Left: " + str(amounts_list[2]))
                self.p2_current_bet_field.setPlainText(str(self.player_bets[2]))                
            elif msg0.id == "p3_cards":
                cards[3] = msg0.content
                print("entered: ", msg0.id, msg0.content)
                self.p3_left_field.setPlainText(str(cards[3][0]))
                self.p3_right_field.setPlainText(str(cards[3][1]))
                self.p3_amount_left_label.setText("Amount Left: " + str(amounts_list[3]))
                self.p3_current_bet_field.setPlainText(str(self.player_bets[3]))
            elif msg0.id == "p4_cards":
                cards[4] = msg0.content
                print("entered: ", msg0.id, msg0.content)
                self.p4_left_field.setPlainText(str(cards[4][0]))
                self.p4_right_field.setPlainText(str(cards[4][1]))
                self.p4_amount_left_label.setText("Amount Left: " + str(amounts_list[4]))
                self.p4_current_bet_field.setPlainText(str(self.player_bets[4]))
            elif msg0.id == "continue":
                print("...GUI received CONTINUE to next round")
                break
            elif msg0.id == "GAME OVER!":
                # end the game
                #self.exit_it() # TESTING (THIS WORKED!!)
                self.timer.stop()
                hb.button_press.disconnect()
                sb.button_press.disconnect()
                db.button_press.disconnect()
                eb.button_press.disconnect()
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
        current_player = "p0"
        self.double_button_clicked = True

        if self.double_button_clicked: # need to make self.bet into a list of bets
        # maybe instead of checking button states, just manually make it go from p1 to p4
            msg = Message("double", self.player_bets)
            gui_to_bj_queue.put(msg)

            while(1):
                msg1 = bj_to_gui_queue.get()
                print("GUI received msg: " + str(msg1.id) + ", Content: " + str(msg1.content))
                current_player = msg1.id

                if msg1.id == "p1_cards":
                    cards[1] = msg1.content[0]
                    self.your_cards_left_field.setPlainText(str(cards[1]))
                    self.your_cards_right_field.setPlainText("")
                    self.current_bet_field.setPlainText(str(msg1.content[1]))
                elif msg1.id == "p2_cards":
                    cards[2] = msg1.content[0]
                    self.p2_left_field.setPlainText(str(cards[2]))
                    self.p2_right_field.setPlainText(str(""))
                    self.p2_current_bet_field.setPlainText(str(msg1.content[1]))
                elif msg1.id == "p3_cards":
                    cards[3] = msg1.content[0]
                    self.p3_left_field.setPlainText(str(cards[3]))
                    self.p3_right_field.setPlainText(str(""))
                    self.p3_current_bet_field.setPlainText(str(msg1.content[1]))
                elif msg1.id == "p4_cards":
                    cards[4] = msg1.content[0]
                    self.p4_left_field.setPlainText(str(cards[4]))
                    self.p4_right_field.setPlainText(str(""))
                    self.p4_current_bet_field.setPlainText(str(msg1.content[1]))
                elif msg1.id == "continue":
                    self.reset_buttons(msg1.content)
                    break
                elif msg1.id == "done_round":
                    # need to go back and reset DOUBLE/STAND/HIT BUTTON functionality
                    self.double_button_clicked == False
                    
                    # need to change this for multiplayer
                    cards[0] = msg1.content[0]
                    scoring = msg1.content[1]
                    wallets = msg1.content[2]

                    for x in range(int(self.numPlayers)+1):
                        amounts_list[x] = wallets[x]
                        if x == 1:
                            self.amount_left_label.setText(str(amounts_list[x]))
                        elif x == 2:
                            self.p2_amount_left_label.setText(str(amounts_list[x]))
                        elif x == 3:
                            self.p3_amount_left_label.setText(str(amounts_list[x]))
                        elif x == 4:
                            self.p4_amount_left_label.setText(str(amounts_list[x]))

                    QtTest.QTest.qWait(DELAYED)
                    # put in the player and dealer cards to display in next round screen
                    #self.reset_buttons()
                    self.open_next_round(scoring, wallets)
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
        print("Player stand. Next Player go.")

        # need to receive which player's turn it is
        print("getting STAND msg from BJ...")
        while(1):
            msg = bj_to_gui_queue.get()
            if msg.id == "done_round":
                print("...received done_round msg from BJ")
                # change these for multiplayer
                cards[0] = msg.content[0]
                scoring = msg.content[1]
                wallets = msg.content[2] # need to update everyone's amount left from wallet

                for x in range(int(self.numPlayers)+1):
                    amounts_list[x] = wallets[x]
                    if x == 1:
                        self.amount_left_label.setText(str(amounts_list[x]))
                    elif x == 2:
                        self.p2_amount_left_label.setText(str(amounts_list[x]))
                    elif x == 3:
                        self.p3_amount_left_label.setText(str(amounts_list[x]))
                    elif x == 4:
                        self.p4_amount_left_label.setText(str(amounts_list[x]))

                QtTest.QTest.qWait(DELAYED)
                # put in the player and dealer cards to display in next round screen
                #self.reset_buttons()
                self.open_next_round(scoring, wallets)
                QtTest.QTest.qWait(DELAYED)
                self.done_round()
                break
            elif msg.id == "continue":
                self.reset_buttons(msg.content)
                print("...received CONTINUE msg from BJ")
                break
        

    # TODO
    # when "HIT" button is pressed, do nothing to current bet, add another card to player
    def hit_it(self):
        # need to change so that the value of button press is sent over; if value is TRUE, update that player's stats
        msg = Message("hit", None) # take in button hit status, traverse through to find which button was pressed, update player stats
        gui_to_bj_queue.put(msg)

        while(1):
            msg = bj_to_gui_queue.get()
            if msg.id == "p1_cards":
                cards[1] = msg.content
                print("p1: ", cards[1])
                self.your_cards_left_field.setPlainText(str(cards[1]))
                self.your_cards_right_field.setPlainText(str(""))
            elif msg.id == "p2_cards":
                cards[2] = msg.content
                print("p2: ", cards[2])
                self.p2_left_field.setPlainText(str(cards[2]))
                self.p2_right_field.setPlainText(str(""))
            elif msg.id == "p3_cards":
                cards[3] = msg.content
                print("p3: ", cards[3])
                self.p3_left_field.setPlainText(str(cards[3]))
                self.p3_right_field.setPlainText(str(""))
            elif msg.id == "p4_cards":
                cards[4] = msg.content
                print("p4: ", cards[4])
                self.p4_left_field.setPlainText(str(cards[4]))
                self.p4_right_field.setPlainText(str(""))
            elif msg.id == "switch":
                self.reset_buttons(msg.content)
            elif msg.id == "continue":
                break
            elif msg.id == "done_round":
                # after every player goes, display the contents of the round
                cards[0] = msg.content[0]
                scoring = msg.content[1]
                wallets = msg.content[2]

                for x in range(int(self.numPlayers)+1):
                    amounts_list[x] = wallets[x]
                    if x == 1:
                        self.amount_left_label.setText(str(amounts_list[x]))
                    elif x == 2:
                        self.p2_amount_left_label.setText(str(amounts_list[x]))
                    elif x == 3:
                        self.p3_amount_left_label.setText(str(amounts_list[x]))
                    elif x == 4:
                        self.p4_amount_left_label.setText(str(amounts_list[x]))

                QtTest.QTest.qWait(DELAYED)
                # put in the player and dealer cards to display in next round screen
                #self.reset_buttons()
                self.open_next_round(scoring, wallets)
                QtTest.QTest.qWait(DELAYED)
                self.done_round()
                break
            else:
                pass
            #self.reset_buttons()
        

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

    # setting up main window and components (for one player)
    # CHANGE THIS FUNCTION DEPENDING ON THE NUMPLAYERS
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        global cards, amounts_list
        
        if str(self.numPlayers) == "1":
            # FOR ONE PLAYER
            ######################################################################
            #
            #
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

            # need to remove dealer aspect?
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

            self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.verticalLayoutWidget.setGeometry(600, 280, 100, 150)
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.hit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.hit_button.setObjectName("hit_button")
            self.hit_button.setText("HIT")
            self.verticalLayout.addWidget(self.hit_button)
            self.double_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.double_it())
            self.double_button.setObjectName("double_button")
            self.double_button.setText("DOUBLE")
            self.verticalLayout.addWidget(self.double_button)
            self.stand_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.stand_button.setObjectName("stand_button")
            self.stand_button.setText("STAND")
            self.verticalLayout.addWidget(self.stand_button)
            self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.exit_button.setObjectName("exit_button")
            self.verticalLayout.addWidget(self.exit_button)
            self.exit_button.setText("EXIT")

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
            self.label.setText("P1 Cards:")
            self.label_3.setText("P1 Bet:")

            self.your_cards_left_field.setPlainText(str(cards[1][0]))
            self.your_cards_right_field.setPlainText(str(cards[1][1]))
            print("P1 first cards: ", cards[1])
            self.amount_left_label.setText("Amount Left: " + str(amounts_list[1]))
            self.current_bet_field.setPlainText(str(self.player_bets[1]))

        #
        #
        #########################################################################

        # FOR TWO PLAYERS
        ######################################################################
        #
        #
        elif str(self.numPlayers) == "2":
            ############# LAYOUTS FOR EACH PLAYER ###########
            # PLAYER 1 CARDS LAYOUT
            self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.your_cards_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
            self.your_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.your_cards_layout.setObjectName("your_cards_layout")
            # PLAYER 1 LABEL CARDS LAYOUT
            self.labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.labelLayoutWidget.setGeometry(140, 130, 150, 100)
            self.labelLayoutWidget.setObjectName("labelLayoutWidget")
            self.labelLayout = QtWidgets.QVBoxLayout(self.labelLayoutWidget)
            self.labelLayout.setContentsMargins(0, 0, 0, 0)
            self.labelLayout.setObjectName("labelLayout")
            # PLAYER 1 BUTTON LAYOUT
            self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.verticalLayoutWidget.setGeometry(300, 130, 70, 100)
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            # PLAYER 1 BET LAYOUT
            self.betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.betLayoutWidget.setGeometry(60, 150, 70, 70)
            self.betLayoutWidget.setObjectName("betLayoutWidget")
            self.betLayout = QtWidgets.QVBoxLayout(self.betLayoutWidget)
            self.betLayout.setContentsMargins(0, 0, 0, 0)
            self.betLayout.setObjectName("betLayout")            

            # PLAYER 2 CARDS LAYOUT
            self.p2_horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.p2_horizontalLayoutWidget.setGeometry(250, 280, 300, 150)
            self.p2_horizontalLayoutWidget.setObjectName("p2_horizontalLayoutWidget")
            self.p2_cards_layout = QtWidgets.QHBoxLayout(self.p2_horizontalLayoutWidget)
            self.p2_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.p2_cards_layout.setObjectName("p2_cards_layout")
            # PLAYER 2 LABEL CARDS LAYOUT
            self.p2_labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_labelLayoutWidget.setGeometry(520, 130, 150, 100)
            self.p2_labelLayoutWidget.setObjectName("p2_labelLayoutWidget")
            self.p2_labelLayout = QtWidgets.QVBoxLayout(self.p2_labelLayoutWidget)
            self.p2_labelLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_labelLayout.setObjectName("p2_labelLayout")
            # PLAYER 2 BUTTON LAYOUT
            self.p2_verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_verticalLayoutWidget.setGeometry(680,130, 70, 100)
            self.p2_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.p2_verticalLayout = QtWidgets.QVBoxLayout(self.p2_verticalLayoutWidget)
            self.p2_verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_verticalLayout.setObjectName("p2_verticalLayout")
            # PLAYER 2 BET LAYOUT
            self.p2_betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_betLayoutWidget.setGeometry(440, 150, 70, 70)
            self.p2_betLayoutWidget.setObjectName("p2_betLayoutWidget")
            self.p2_betLayout = QtWidgets.QVBoxLayout(self.p2_betLayoutWidget)
            self.p2_betLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_betLayout.setObjectName("p2_betLayout")


            ########### CURRENT BET LAYOUT ##########
            # PLAYER 1
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            #self.label_3.setGeometry(110, 15, 110, 110)
            self.label_3.setObjectName("label_3")
            self.label_3.setFont(font10)
            self.label_3.setText("P1 Bet:")
            self.betLayout.addWidget(self.label_3)
            self.current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.current_bet_field.setFont(font20)
            self.current_bet_field.setObjectName("current_bet_field")
            self.betLayout.addWidget(self.current_bet_field)
            #self.p1_layout.addWidget(self.betLayoutWidget)

            # PLAYER 2
            self.p2_label_2 = QtWidgets.QLabel(self.centralwidget)
            self.p2_label_2.setObjectName("p2_label_2")
            self.p2_label_2.setFont(font10)
            self.p2_label_2.setText("P2 Bet:")
            self.p2_betLayout.addWidget(self.p2_label_2)
            self.p2_current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.p2_current_bet_field.setFont(font20)
            self.p2_current_bet_field.setObjectName("p2_current_bet_field")
            self.p2_betLayout.addWidget(self.p2_current_bet_field)

            ########### PLAYING CARD FIELDS ###########

            # PLAYER 1
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setObjectName("label")
            self.label.setFont(font10)
            self.label.setText("P1 Cards:")
            self.labelLayout.addWidget(self.label)
            self.your_cards_left_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget, readOnly=True)
            self.your_cards_left_field.setObjectName("your_cards_left_field")
            self.your_cards_left_field.setFont(font20)
            self.your_cards_layout.addWidget(self.your_cards_left_field)
            self.your_cards_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget, readOnly=True)
            self.your_cards_right_field.setObjectName("your_cards_right_field")
            self.your_cards_right_field.setFont(font20)
            self.your_cards_layout.addWidget(self.your_cards_right_field)
            self.labelLayout.addWidget(self.horizontalLayoutWidget)
            #self.p1_layout.addWidget(self.labelLayoutWidget)

            # PLAYER 2
            self.p2_label = QtWidgets.QLabel(self.centralwidget)
            self.p2_label.setObjectName("p2_label")
            self.p2_label.setFont(font10)
            self.p2_label.setText("P2 Cards:")
            self.p2_labelLayout.addWidget(self.p2_label)
            self.p2_left_field = QtWidgets.QPlainTextEdit(self.p2_horizontalLayoutWidget, readOnly=True)
            self.p2_left_field.setObjectName("p2_left_field")
            self.p2_left_field.setFont(font20)
            self.p2_cards_layout.addWidget(self.p2_left_field)
            self.p2_right_field = QtWidgets.QPlainTextEdit(self.p2_horizontalLayoutWidget, readOnly=True)
            self.p2_right_field.setObjectName("p2_right_field")
            self.p2_right_field.setFont(font20)
            self.p2_cards_layout.addWidget(self.p2_right_field)
            self.p2_labelLayout.addWidget(self.p2_horizontalLayoutWidget)

            ############### PLAYER VERTICAL BUTTONS ################

            # PLAYER 1 AMOUNT LEFT
            self.amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.amount_left_label.setFont(font6)
            self.amount_left_label.setObjectName("amount_left_label")
            self.amount_left_label.setText(("Amount Left: ") + str(amounts_list[1]))
            self.verticalLayout.addWidget(self.amount_left_label)
            # PLAYER 1 HIT
            self.hit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.hit_button.setObjectName("hit_button")
            self.hit_button.setText("HIT")
            self.verticalLayout.addWidget(self.hit_button)
            # PLAYER 1 DOUBLE
            self.double_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.double_it())
            self.double_button.setObjectName("double_button")
            self.double_button.setText("DOUBLE")
            self.verticalLayout.addWidget(self.double_button)
            # PLAYER 1 STAND
            self.stand_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.stand_button.setObjectName("stand_button")
            self.stand_button.setText("STAND")
            self.verticalLayout.addWidget(self.stand_button)
            # PLAYER 1
            self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.exit_button.setObjectName("exit_button")
            self.exit_button.setText("EXIT")
            self.verticalLayout.addWidget(self.exit_button)
            #self.p1_layout.addWidget(self.verticalLayoutWidget)


            # PLAYER 2 AMOUNT LEFT
            self.p2_amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.p2_amount_left_label.setFont(font6)
            self.p2_amount_left_label.setObjectName("p2_amount_left_label")
            self.p2_amount_left_label.setText(("Amount Left: ") + str(amounts_list[2]))
            self.p2_verticalLayout.addWidget(self.p2_amount_left_label)
            # PLAYER 2 HIT
            self.p2_hit_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.p2_hit_button.setObjectName("p2_hit_button")
            self.p2_hit_button.setText("HIT")
            self.p2_verticalLayout.addWidget(self.p2_hit_button)
            # PLAYER 2 DOUBLE
            self.p2_double_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.double_it())
            self.p2_double_button.setObjectName("p2_double_button")
            self.p2_double_button.setText("DOUBLE")
            self.p2_verticalLayout.addWidget(self.p2_double_button)
            # PLAYER 2 STAND
            self.p2_stand_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.p2_stand_button.setObjectName("p2_stand_button")
            self.p2_stand_button.setText("STAND")
            self.p2_verticalLayout.addWidget(self.p2_stand_button)
            # PLAYER 2
            self.p2_exit_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.p2_exit_button.setObjectName("p2_exit_button")
            self.p2_exit_button.setText("EXIT")
            self.p2_verticalLayout.addWidget(self.p2_exit_button)

            #print(cards)
            self.your_cards_left_field.setPlainText(str(cards[1][0]))
            self.your_cards_right_field.setPlainText(str(cards[1][1]))
            print("P1 first cards: ", cards[1])
            self.amount_left_label.setText("Amount Left: " + str(amounts_list[1]))
            self.current_bet_field.setPlainText(str(self.player_bets[1]))

            self.p2_left_field.setPlainText(str(cards[2][0]))
            self.p2_right_field.setPlainText(str(cards[2][1]))
            print("P2 first cards: ", cards[2])
            self.p2_amount_left_label.setText("Amount Left: " + str(amounts_list[2]))
            self.p2_current_bet_field.setPlainText(str(self.player_bets[2]))

        #
        #
        #########################################################################

        # FOR THREE PLAYERS
        ######################################################################
        #
        #
        elif str(self.numPlayers) == "3":
            ############# LAYOUTS FOR EACH PLAYER ###########
            # PLAYER 1 CARDS LAYOUT
            self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.horizontalLayoutWidget.setGeometry(100, 70, 300, 150)
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.your_cards_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
            self.your_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.your_cards_layout.setObjectName("your_cards_layout")
            # PLAYER 1 LABEL CARDS LAYOUT
            self.labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.labelLayoutWidget.setGeometry(140, 70, 150, 100)
            self.labelLayoutWidget.setObjectName("labelLayoutWidget")
            self.labelLayout = QtWidgets.QVBoxLayout(self.labelLayoutWidget)
            self.labelLayout.setContentsMargins(0, 0, 0, 0)
            self.labelLayout.setObjectName("labelLayout")
            # PLAYER 1 BUTTON LAYOUT
            self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.verticalLayoutWidget.setGeometry(300, 70, 70, 100)
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            # PLAYER 1 BET LAYOUT
            self.betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.betLayoutWidget.setGeometry(60, 90, 70, 70)
            self.betLayoutWidget.setObjectName("betLayoutWidget")
            self.betLayout = QtWidgets.QVBoxLayout(self.betLayoutWidget)
            self.betLayout.setContentsMargins(0, 0, 0, 0)
            self.betLayout.setObjectName("betLayout")            

            # PLAYER 2 CARDS LAYOUT
            self.p2_horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.p2_horizontalLayoutWidget.setGeometry(250, 280, 300, 150)
            self.p2_horizontalLayoutWidget.setObjectName("p2_horizontalLayoutWidget")
            self.p2_cards_layout = QtWidgets.QHBoxLayout(self.p2_horizontalLayoutWidget)
            self.p2_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.p2_cards_layout.setObjectName("p2_cards_layout")
            # PLAYER 2 LABEL CARDS LAYOUT
            self.p2_labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_labelLayoutWidget.setGeometry(520, 70, 150, 100)
            self.p2_labelLayoutWidget.setObjectName("p2_labelLayoutWidget")
            self.p2_labelLayout = QtWidgets.QVBoxLayout(self.p2_labelLayoutWidget)
            self.p2_labelLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_labelLayout.setObjectName("p2_labelLayout")
            # PLAYER 2 BUTTON LAYOUT
            self.p2_verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_verticalLayoutWidget.setGeometry(680, 70, 70, 100)
            self.p2_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.p2_verticalLayout = QtWidgets.QVBoxLayout(self.p2_verticalLayoutWidget)
            self.p2_verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_verticalLayout.setObjectName("p2_verticalLayout")
            # PLAYER 2 BET LAYOUT
            self.p2_betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_betLayoutWidget.setGeometry(440, 90, 70, 70)
            self.p2_betLayoutWidget.setObjectName("p2_betLayoutWidget")
            self.p2_betLayout = QtWidgets.QVBoxLayout(self.p2_betLayoutWidget)
            self.p2_betLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_betLayout.setObjectName("p2_betLayout")

            # PLAYER 3 CARDS LAYOUT
            self.p3_horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_horizontalLayoutWidget.setObjectName("p3_horizontalLayoutWidget")
            self.p3_cards_layout = QtWidgets.QHBoxLayout(self.p3_horizontalLayoutWidget)
            self.p3_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.p3_cards_layout.setObjectName("p3_cards_layout")
            # PLAYER 3 LABEL CARDS LAYOUT
            self.p3_labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_labelLayoutWidget.setGeometry(325, 280, 150, 100)
            self.p3_labelLayoutWidget.setObjectName("p3_labelLayoutWidget")
            self.p3_labelLayout = QtWidgets.QVBoxLayout(self.p3_labelLayoutWidget)
            self.p3_labelLayout.setContentsMargins(0, 0, 0, 0)
            self.p3_labelLayout.setObjectName("p3_labelLayout")
            # PLAYER 3 BUTTON LAYOUT
            self.p3_verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_verticalLayoutWidget.setGeometry(485, 280, 70, 100)
            self.p3_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.p3_verticalLayout = QtWidgets.QVBoxLayout(self.p3_verticalLayoutWidget)
            self.p3_verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.p3_verticalLayout.setObjectName("p3_verticalLayout")
            # PLAYER 3 BET LAYOUT
            self.p3_betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_betLayoutWidget.setGeometry(245, 300, 70, 70)
            self.p3_betLayoutWidget.setObjectName("p3_betLayoutWidget")
            self.p3_betLayout = QtWidgets.QVBoxLayout(self.p3_betLayoutWidget)
            self.p3_betLayout.setContentsMargins(0, 0, 0, 0)
            self.p3_betLayout.setObjectName("p3_betLayout")

            ########### CURRENT BET LAYOUT ##########
            # PLAYER 1
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            #self.label_3.setGeometry(110, 15, 110, 110)
            self.label_3.setObjectName("label_3")
            self.label_3.setFont(font10)
            self.label_3.setText("P1 Bet:")
            self.betLayout.addWidget(self.label_3)
            self.current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.current_bet_field.setFont(font20)
            self.current_bet_field.setObjectName("current_bet_field")
            self.betLayout.addWidget(self.current_bet_field)
            #self.p1_layout.addWidget(self.betLayoutWidget)

            # PLAYER 2
            self.p2_label_2 = QtWidgets.QLabel(self.centralwidget)
            self.p2_label_2.setObjectName("p2_label_2")
            self.p2_label_2.setFont(font10)
            self.p2_label_2.setText("P2 Bet:")
            self.p2_betLayout.addWidget(self.p2_label_2)
            self.p2_current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.p2_current_bet_field.setFont(font20)
            self.p2_current_bet_field.setObjectName("p2_current_bet_field")
            self.p2_betLayout.addWidget(self.p2_current_bet_field)

            # PLAYER 3
            self.p3_label_2 = QtWidgets.QLabel(self.centralwidget)
            self.p3_label_2.setObjectName("p3_label_2")
            self.p3_label_2.setFont(font10)
            self.p3_label_2.setText("P3 Bet:")
            self.p3_betLayout.addWidget(self.p3_label_2)
            self.p3_current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.p3_current_bet_field.setFont(font20)
            self.p3_current_bet_field.setObjectName("p3_current_bet_field")
            self.p3_betLayout.addWidget(self.p3_current_bet_field)

            ########### PLAYING CARD FIELDS ###########

            # PLAYER 1
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setObjectName("label")
            self.label.setFont(font10)
            self.label.setText("P1 Cards:")
            self.labelLayout.addWidget(self.label)
            self.your_cards_left_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget, readOnly=True)
            self.your_cards_left_field.setObjectName("your_cards_left_field")
            self.your_cards_left_field.setFont(font20)
            self.your_cards_layout.addWidget(self.your_cards_left_field)
            self.your_cards_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget, readOnly=True)
            self.your_cards_right_field.setObjectName("your_cards_right_field")
            self.your_cards_right_field.setFont(font20)
            self.your_cards_layout.addWidget(self.your_cards_right_field)
            self.labelLayout.addWidget(self.horizontalLayoutWidget)
            #self.p1_layout.addWidget(self.labelLayoutWidget)

            # PLAYER 2
            self.p2_label = QtWidgets.QLabel(self.centralwidget)
            self.p2_label.setObjectName("p2_label")
            self.p2_label.setFont(font10)
            self.p2_label.setText("P2 Cards:")
            self.p2_labelLayout.addWidget(self.p2_label)
            self.p2_left_field = QtWidgets.QPlainTextEdit(self.p2_horizontalLayoutWidget, readOnly=True)
            self.p2_left_field.setObjectName("p2_left_field")
            self.p2_left_field.setFont(font20)
            self.p2_cards_layout.addWidget(self.p2_left_field)
            self.p2_right_field = QtWidgets.QPlainTextEdit(self.p2_horizontalLayoutWidget, readOnly=True)
            self.p2_right_field.setObjectName("p2_right_field")
            self.p2_right_field.setFont(font20)
            self.p2_cards_layout.addWidget(self.p2_right_field)
            self.p2_labelLayout.addWidget(self.p2_horizontalLayoutWidget)

            # PLAYER 3
            self.p3_label = QtWidgets.QLabel(self.centralwidget)
            self.p3_label.setObjectName("p3_label")
            self.p3_label.setFont(font10)
            self.p3_label.setText("P3 Cards:")
            self.p3_labelLayout.addWidget(self.p3_label)
            self.p3_left_field = QtWidgets.QPlainTextEdit(self.p3_horizontalLayoutWidget, readOnly=True)
            self.p3_left_field.setObjectName("p3_left_field")
            self.p3_left_field.setFont(font20)
            self.p3_cards_layout.addWidget(self.p3_left_field)
            self.p3_right_field = QtWidgets.QPlainTextEdit(self.p3_horizontalLayoutWidget, readOnly=True)
            self .p3_right_field.setObjectName("p3_right_field")
            self.p3_right_field.setFont(font20)
            self.p3_cards_layout.addWidget(self.p3_right_field)
            self.p3_labelLayout.addWidget(self.p3_horizontalLayoutWidget)

            ############### PLAYER VERTICAL BUTTONS ################

            # PLAYER 1 AMOUNT LEFT
            self.amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.amount_left_label.setFont(font6)
            self.amount_left_label.setObjectName("amount_left_label")
            self.amount_left_label.setText(("Amount Left: ") + str(amounts_list[1]))
            self.verticalLayout.addWidget(self.amount_left_label)
            # PLAYER 1 HIT
            self.hit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.hit_button.setObjectName("hit_button")
            self.hit_button.setText("HIT")
            self.verticalLayout.addWidget(self.hit_button)
            # PLAYER 1 DOUBLE
            self.double_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.double_it())
            self.double_button.setObjectName("double_button")
            self.double_button.setText("DOUBLE")
            self.verticalLayout.addWidget(self.double_button)
            # PLAYER 1 STAND
            self.stand_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.stand_button.setObjectName("stand_button")
            self.stand_button.setText("STAND")
            self.verticalLayout.addWidget(self.stand_button)
            # PLAYER 1
            self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.exit_button.setObjectName("exit_button")
            self.exit_button.setText("EXIT")
            self.verticalLayout.addWidget(self.exit_button)
            #self.p1_layout.addWidget(self.verticalLayoutWidget)


            # PLAYER 2 AMOUNT LEFT
            self.p2_amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.p2_amount_left_label.setFont(font6)
            self.p2_amount_left_label.setObjectName("p2_amount_left_label")
            self.p2_amount_left_label.setText(("Amount Left: ") + str(amounts_list[2]))
            self.p2_verticalLayout.addWidget(self.p2_amount_left_label)
            # PLAYER 2 HIT
            self.p2_hit_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.p2_hit_button.setObjectName("p2_hit_button")
            self.p2_hit_button.setText("HIT")
            self.p2_verticalLayout.addWidget(self.p2_hit_button)
            # PLAYER 2 DOUBLE
            self.p2_double_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.double_it())
            self.p2_double_button.setObjectName("p2_double_button")
            self.p2_double_button.setText("DOUBLE")
            self.p2_verticalLayout.addWidget(self.p2_double_button)
            # PLAYER 2 STAND
            self.p2_stand_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.p2_stand_button.setObjectName("p2_stand_button")
            self.p2_stand_button.setText("STAND")
            self.p2_verticalLayout.addWidget(self.p2_stand_button)
            # PLAYER 2
            self.p2_exit_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.p2_exit_button.setObjectName("p2_exit_button")
            self.p2_exit_button.setText("EXIT")
            self.p2_verticalLayout.addWidget(self.p2_exit_button)

            # PLAYER 3 AMOUNT LEFT
            self.p3_amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.p3_amount_left_label.setFont(font6)
            self.p3_amount_left_label.setObjectName("p3_amount_left_label")
            self.p3_amount_left_label.setText(("Amount Left: ") + str(amounts_list[3]))
            self.p3_verticalLayout.addWidget(self.p3_amount_left_label)
            # PLAYER 3 HIT
            self.p3_hit_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.p3_hit_button.setObjectName("p3_hit_button")
            self.p3_verticalLayout.addWidget(self.p3_hit_button)
            self.p3_hit_button.setText("HIT")
            # PLAYER 3 DOUBLE
            self.p3_double_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.double_it())
            self.p3_double_button.setObjectName("p3_double_button")
            self.p3_double_button.setText("DOUBLE")
            self.p3_verticalLayout.addWidget(self.p3_double_button)
            # PLAYER 3 STAND
            self.p3_stand_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.p3_stand_button.setObjectName("p3_stand_button")
            self.p3_stand_button.setText("STAND")
            self.p3_verticalLayout.addWidget(self.p3_stand_button)
            # PLAYER 3
            self.p3_exit_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.p3_exit_button.setObjectName("p3_exit_button")
            self.p3_exit_button.setText("EXIT")
            self.p3_verticalLayout.addWidget(self.p3_exit_button)

            self.your_cards_left_field.setPlainText(str(cards[1][0]))
            self.your_cards_right_field.setPlainText(str(cards[1][1]))
            print("P1 first cards: ", cards[1])
            self.amount_left_label.setText("Amount Left: " + str(amounts_list[1]))
            self.current_bet_field.setPlainText(str(self.player_bets[1]))

            self.p2_left_field.setPlainText(str(cards[2][0]))
            self.p2_right_field.setPlainText(str(cards[2][1]))
            print("P2 first cards: ", cards[2])
            self.p2_amount_left_label.setText("Amount Left: " + str(amounts_list[2]))
            self.p2_current_bet_field.setPlainText(str(self.player_bets[2]))

            self.p3_left_field.setPlainText(str(cards[3][0]))
            self.p3_right_field.setPlainText(str(cards[3][1]))
            print("P3 first cards: ", cards[3])
            self.p3_amount_left_label.setText("Amount Left: " + str(amounts_list[3]))
            self.p3_current_bet_field.setPlainText(str(self.player_bets[3]))

        #
        #
        #########################################################################

        # FOR FOUR PLAYERS
        ######################################################################
        #
        #
        elif str(self.numPlayers) == "4":
            ############# LAYOUTS FOR EACH PLAYER ###########
            # PLAYER 1 CARDS LAYOUT
            self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.horizontalLayoutWidget.setGeometry(100, 70, 300, 150)
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.your_cards_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
            self.your_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.your_cards_layout.setObjectName("your_cards_layout")
            # PLAYER 1 LABEL CARDS LAYOUT
            self.labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.labelLayoutWidget.setGeometry(140, 70, 150, 100)
            self.labelLayoutWidget.setObjectName("labelLayoutWidget")
            self.labelLayout = QtWidgets.QVBoxLayout(self.labelLayoutWidget)
            self.labelLayout.setContentsMargins(0, 0, 0, 0)
            self.labelLayout.setObjectName("labelLayout")
            # PLAYER 1 BUTTON LAYOUT
            self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.verticalLayoutWidget.setGeometry(300, 70, 70, 100)
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            # PLAYER 1 BET LAYOUT
            self.betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.betLayoutWidget.setGeometry(60, 90, 70, 70)
            self.betLayoutWidget.setObjectName("betLayoutWidget")
            self.betLayout = QtWidgets.QVBoxLayout(self.betLayoutWidget)
            self.betLayout.setContentsMargins(0, 0, 0, 0)
            self.betLayout.setObjectName("betLayout")            

            # PLAYER 2 CARDS LAYOUT
            self.p2_horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.p2_horizontalLayoutWidget.setGeometry(250, 280, 300, 150)
            self.p2_horizontalLayoutWidget.setObjectName("p2_horizontalLayoutWidget")
            self.p2_cards_layout = QtWidgets.QHBoxLayout(self.p2_horizontalLayoutWidget)
            self.p2_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.p2_cards_layout.setObjectName("p2_cards_layout")
            # PLAYER 2 LABEL CARDS LAYOUT
            self.p2_labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_labelLayoutWidget.setGeometry(520, 70, 150, 100)
            self.p2_labelLayoutWidget.setObjectName("p2_labelLayoutWidget")
            self.p2_labelLayout = QtWidgets.QVBoxLayout(self.p2_labelLayoutWidget)
            self.p2_labelLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_labelLayout.setObjectName("p2_labelLayout")
            # PLAYER 2 BUTTON LAYOUT
            self.p2_verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_verticalLayoutWidget.setGeometry(680, 70, 70, 100)
            self.p2_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.p2_verticalLayout = QtWidgets.QVBoxLayout(self.p2_verticalLayoutWidget)
            self.p2_verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_verticalLayout.setObjectName("p2_verticalLayout")
            # PLAYER 2 BET LAYOUT
            self.p2_betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p2_betLayoutWidget.setGeometry(440, 90, 70, 70)
            self.p2_betLayoutWidget.setObjectName("p2_betLayoutWidget")
            self.p2_betLayout = QtWidgets.QVBoxLayout(self.p2_betLayoutWidget)
            self.p2_betLayout.setContentsMargins(0, 0, 0, 0)
            self.p2_betLayout.setObjectName("p2_betLayout")

            # PLAYER 3 CARDS LAYOUT
            self.p3_horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.p3_horizontalLayoutWidget.setGeometry(250, 280, 300, 150)
            self.p3_horizontalLayoutWidget.setObjectName("p3_horizontalLayoutWidget")
            self.p3_cards_layout = QtWidgets.QHBoxLayout(self.p3_horizontalLayoutWidget)
            self.p3_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.p3_cards_layout.setObjectName("p3_cards_layout")
            # PLAYER 3 LABEL CARDS LAYOUT
            self.p3_labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_labelLayoutWidget.setGeometry(140, 290, 150, 100)
            self.p3_labelLayoutWidget.setObjectName("p3_labelLayoutWidget")
            self.p3_labelLayout = QtWidgets.QVBoxLayout(self.p3_labelLayoutWidget)
            self.p3_labelLayout.setContentsMargins(0, 0, 0, 0)
            self.p3_labelLayout.setObjectName("p3_labelLayout")
            # PLAYER 3 BUTTON LAYOUT
            self.p3_verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_verticalLayoutWidget.setGeometry(300, 290, 70, 100)
            self.p3_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.p3_verticalLayout = QtWidgets.QVBoxLayout(self.p3_verticalLayoutWidget)
            self.p3_verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.p3_verticalLayout.setObjectName("p3_verticalLayout")
            # PLAYER 3 BET LAYOUT
            self.p3_betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p3_betLayoutWidget.setGeometry(60, 310, 70, 70)
            self.p3_betLayoutWidget.setObjectName("p3_betLayoutWidget")
            self.p3_betLayout = QtWidgets.QVBoxLayout(self.p3_betLayoutWidget)
            self.p3_betLayout.setContentsMargins(0, 0, 0, 0)
            self.p3_betLayout.setObjectName("p3_betLayout")

            # PLAYER 4 CARDS LAYOUT
            self.p4_horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            #self.p4_horizontalLayoutWidget.setGeometry(250, 280, 300, 150)
            self.p4_horizontalLayoutWidget.setObjectName("p4_horizontalLayoutWidget")
            self.p4_cards_layout = QtWidgets.QHBoxLayout(self.p4_horizontalLayoutWidget)
            self.p4_cards_layout.setContentsMargins(0, 0, 0, 0)
            self.p4_cards_layout.setObjectName("p4_cards_layout")
            # PLAYER 4 LABEL CARDS LAYOUT
            self.p4_labelLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p4_labelLayoutWidget.setGeometry(520, 290, 150, 100)
            self.p4_labelLayoutWidget.setObjectName("p4_labelLayoutWidget")
            self.p4_labelLayout = QtWidgets.QVBoxLayout(self.p4_labelLayoutWidget)
            self.p4_labelLayout.setContentsMargins(0, 0, 0, 0)
            self.p4_labelLayout.setObjectName("p4_labelLayout")
            # PLAYER 4 BUTTON LAYOUT
            self.p4_verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p4_verticalLayoutWidget.setGeometry(680, 290, 70, 100)
            self.p4_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.p4_verticalLayout = QtWidgets.QVBoxLayout(self.p4_verticalLayoutWidget)
            self.p4_verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.p4_verticalLayout.setObjectName("p4_verticalLayout")
            # PLAYER 4 BET LAYOUT
            self.p4_betLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.p4_betLayoutWidget.setGeometry(440, 310, 70, 70)
            self.p4_betLayoutWidget.setObjectName("p4_betLayoutWidget")
            self.p4_betLayout = QtWidgets.QVBoxLayout(self.p4_betLayoutWidget)
            self.p4_betLayout.setContentsMargins(0, 0, 0, 0)
            self.p4_betLayout.setObjectName("p4_betLayout")


            ########### CURRENT BET LAYOUT ##########
            # PLAYER 1
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            #self.label_3.setGeometry(110, 15, 110, 110)
            self.label_3.setObjectName("label_3")
            self.label_3.setFont(font10)
            self.label_3.setText("P1 Bet:")
            self.betLayout.addWidget(self.label_3)
            self.current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.current_bet_field.setFont(font20)
            self.current_bet_field.setObjectName("current_bet_field")
            self.betLayout.addWidget(self.current_bet_field)
            #self.p1_layout.addWidget(self.betLayoutWidget)

            # PLAYER 2
            self.p2_label_2 = QtWidgets.QLabel(self.centralwidget)
            self.p2_label_2.setObjectName("p2_label_2")
            self.p2_label_2.setFont(font10)
            self.p2_label_2.setText("P2 Bet:")
            self.p2_betLayout.addWidget(self.p2_label_2)
            self.p2_current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.p2_current_bet_field.setFont(font20)
            self.p2_current_bet_field.setObjectName("p2_current_bet_field")
            self.p2_betLayout.addWidget(self.p2_current_bet_field)

            # PLAYER 3
            self.p3_label_2 = QtWidgets.QLabel(self.centralwidget)
            self.p3_label_2.setObjectName("p3_label_2")
            self.p3_label_2.setFont(font10)
            self.p3_label_2.setText("P3 Bet:")
            self.p3_betLayout.addWidget(self.p3_label_2)
            self.p3_current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.p3_current_bet_field.setFont(font20)
            self.p3_current_bet_field.setObjectName("p3_current_bet_field")
            self.p3_betLayout.addWidget(self.p3_current_bet_field)

            # PLAYER 4
            self.p4_label_2 = QtWidgets.QLabel(self.centralwidget)
            self.p4_label_2.setObjectName("p4_label_2")
            self.p4_label_2.setFont(font10)
            self.p4_label_2.setText("P4 Bet:") 
            self.p4_betLayout.addWidget(self.p4_label_2)
            self.p4_current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget, readOnly=True)
            self.p4_current_bet_field.setFont(font20)
            self.p4_current_bet_field.setObjectName("p4_current_bet_field")  
            self.p4_betLayout.addWidget(self.p4_current_bet_field)  


            ########### PLAYING CARD FIELDS ###########

            # PLAYER 1
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setObjectName("label")
            self.label.setFont(font10)
            self.label.setText("P1 Cards:")
            self.labelLayout.addWidget(self.label)
            self.your_cards_left_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget, readOnly=True)
            self.your_cards_left_field.setObjectName("your_cards_left_field")
            self.your_cards_left_field.setFont(font20)
            self.your_cards_layout.addWidget(self.your_cards_left_field)
            self.your_cards_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget, readOnly=True)
            self.your_cards_right_field.setObjectName("your_cards_right_field")
            self.your_cards_right_field.setFont(font20)
            self.your_cards_layout.addWidget(self.your_cards_right_field)
            self.labelLayout.addWidget(self.horizontalLayoutWidget)
            #self.p1_layout.addWidget(self.labelLayoutWidget)

            # PLAYER 2
            self.p2_label = QtWidgets.QLabel(self.centralwidget)
            self.p2_label.setObjectName("p2_label")
            self.p2_label.setFont(font10)
            self.p2_label.setText("P2 Cards:")
            self.p2_labelLayout.addWidget(self.p2_label)
            self.p2_left_field = QtWidgets.QPlainTextEdit(self.p2_horizontalLayoutWidget, readOnly=True)
            self.p2_left_field.setObjectName("p2_left_field")
            self.p2_left_field.setFont(font20)
            self.p2_cards_layout.addWidget(self.p2_left_field)
            self.p2_right_field = QtWidgets.QPlainTextEdit(self.p2_horizontalLayoutWidget, readOnly=True)
            self.p2_right_field.setObjectName("p2_right_field")
            self.p2_right_field.setFont(font20)
            self.p2_cards_layout.addWidget(self.p2_right_field)
            self.p2_labelLayout.addWidget(self.p2_horizontalLayoutWidget)

            # PLAYER 3
            self.p3_label = QtWidgets.QLabel(self.centralwidget)
            self.p3_label.setObjectName("p3_label")
            self.p3_label.setFont(font10)
            self.p3_label.setText("P3 Cards:")
            self.p3_labelLayout.addWidget(self.p3_label)
            self.p3_left_field = QtWidgets.QPlainTextEdit(self.p3_horizontalLayoutWidget, readOnly=True)
            self.p3_left_field.setObjectName("p3_left_field")
            self.p3_left_field.setFont(font20)
            self.p3_cards_layout.addWidget(self.p3_left_field)
            self.p3_right_field = QtWidgets.QPlainTextEdit(self.p3_horizontalLayoutWidget, readOnly=True)
            self .p3_right_field.setObjectName("p3_right_field")
            self.p3_right_field.setFont(font20)
            self.p3_cards_layout.addWidget(self.p3_right_field)
            self.p3_labelLayout.addWidget(self.p3_horizontalLayoutWidget)

            # PLAYER 4
            self.p4_label = QtWidgets.QLabel(self.centralwidget)
            self.p4_label.setObjectName("p4_label")
            self.p4_label.setFont(font10)
            self.p4_label.setText("P4 Cards:")
            self.p4_labelLayout.addWidget(self.p4_label)
            self.p4_left_field = QtWidgets.QPlainTextEdit(self.p4_horizontalLayoutWidget, readOnly=True)
            self.p4_left_field.setObjectName("p4_left_field")
            self.p4_left_field.setFont(font20)
            self.p4_cards_layout.addWidget(self.p4_left_field)
            self.p4_right_field = QtWidgets.QPlainTextEdit(self.p4_horizontalLayoutWidget, readOnly=True)
            self.p4_right_field.setObjectName("p4_right_field")
            self.p4_right_field.setFont(font20)
            self.p4_cards_layout.addWidget(self.p4_right_field)
            self.p4_labelLayout.addWidget(self.p4_horizontalLayoutWidget)


            ############### PLAYER VERTICAL BUTTONS ################

            # PLAYER 1 AMOUNT LEFT
            self.amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.amount_left_label.setFont(font6)
            self.amount_left_label.setObjectName("amount_left_label")
            self.amount_left_label.setText(("Amount Left: ") + str(amounts_list[1]))
            self.verticalLayout.addWidget(self.amount_left_label)
            # PLAYER 1 HIT
            self.hit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.hit_button.setObjectName("hit_button")
            self.hit_button.setText("HIT")
            self.verticalLayout.addWidget(self.hit_button)
            # PLAYER 1 DOUBLE
            self.double_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.double_it())
            self.double_button.setObjectName("double_button")
            self.double_button.setText("DOUBLE")
            self.verticalLayout.addWidget(self.double_button)
            # PLAYER 1 STAND
            self.stand_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.stand_button.setObjectName("stand_button")
            self.stand_button.setText("STAND")
            self.verticalLayout.addWidget(self.stand_button)
            # PLAYER 1
            self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.exit_button.setObjectName("exit_button")
            self.exit_button.setText("EXIT")
            self.verticalLayout.addWidget(self.exit_button)
            #self.p1_layout.addWidget(self.verticalLayoutWidget)


            # PLAYER 2 AMOUNT LEFT
            self.p2_amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.p2_amount_left_label.setFont(font6)
            self.p2_amount_left_label.setObjectName("p2_amount_left_label")
            self.p2_amount_left_label.setText(("Amount Left: ") + str(amounts_list[2]))
            self.p2_verticalLayout.addWidget(self.p2_amount_left_label)
            # PLAYER 2 HIT
            self.p2_hit_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.p2_hit_button.setObjectName("p2_hit_button")
            self.p2_hit_button.setText("HIT")
            self.p2_verticalLayout.addWidget(self.p2_hit_button)
            # PLAYER 2 DOUBLE
            self.p2_double_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.double_it())
            self.p2_double_button.setObjectName("p2_double_button")
            self.p2_double_button.setText("DOUBLE")
            self.p2_verticalLayout.addWidget(self.p2_double_button)
            # PLAYER 2 STAND
            self.p2_stand_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.p2_stand_button.setObjectName("p2_stand_button")
            self.p2_stand_button.setText("STAND")
            self.p2_verticalLayout.addWidget(self.p2_stand_button)
            # PLAYER 2
            self.p2_exit_button = QtWidgets.QPushButton(self.p2_verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.p2_exit_button.setObjectName("p2_exit_button")
            self.p2_exit_button.setText("EXIT")
            self.p2_verticalLayout.addWidget(self.p2_exit_button)

            # PLAYER 3 AMOUNT LEFT
            self.p3_amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.p3_amount_left_label.setFont(font6)
            self.p3_amount_left_label.setObjectName("p3_amount_left_label")
            self.p3_amount_left_label.setText(("Amount Left: ") + str(amounts_list[3]))
            self.p3_verticalLayout.addWidget(self.p3_amount_left_label)
            # PLAYER 3 HIT
            self.p3_hit_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.p3_hit_button.setObjectName("p3_hit_button")
            self.p3_verticalLayout.addWidget(self.p3_hit_button)
            self.p3_hit_button.setText("HIT")
            # PLAYER 3 DOUBLE
            self.p3_double_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.double_it())
            self.p3_double_button.setObjectName("p3_double_button")
            self.p3_double_button.setText("DOUBLE")
            self.p3_verticalLayout.addWidget(self.p3_double_button)
            # PLAYER 3 STAND
            self.p3_stand_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.p3_stand_button.setObjectName("p3_stand_button")
            self.p3_stand_button.setText("STAND")
            self.p3_verticalLayout.addWidget(self.p3_stand_button)
            # PLAYER 3
            self.p3_exit_button = QtWidgets.QPushButton(self.p3_verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.p3_exit_button.setObjectName("p3_exit_button")
            self.p3_exit_button.setText("EXIT")
            self.p3_verticalLayout.addWidget(self.p3_exit_button)

            # PLAYER 4 AMOUNT LEFT
            self.p4_amount_left_label = QtWidgets.QLabel(self.centralwidget)
            self.p4_amount_left_label.setFont(font6)
            self.p4_amount_left_label.setObjectName("p4_amount_left_label")
            self.p4_amount_left_label.setText(("Amount Left: ") + str(amounts_list[4]))
            self.p4_verticalLayout.addWidget(self.p4_amount_left_label)
            # PLAYER 4 HIT
            self.p4_hit_button = QtWidgets.QPushButton(self.p4_verticalLayoutWidget, clicked=lambda: self.hit_it())
            self.p4_hit_button.setObjectName("p4_hit_button")
            self.p4_verticalLayout.addWidget(self.p4_hit_button)
            self.p4_hit_button.setText("HIT")
            # PLAYER 4 DOUBLE
            self.p4_double_button = QtWidgets.QPushButton(self.p4_verticalLayoutWidget, clicked=lambda: self.double_it())
            self.p4_double_button.setObjectName("p4_double_button")
            self.p4_double_button.setText("DOUBLE")
            self.p4_verticalLayout.addWidget(self.p4_double_button)
            # PLAYER 4 STAND
            self.p4_stand_button = QtWidgets.QPushButton(self.p4_verticalLayoutWidget, clicked=lambda: self.stand_it())
            self.p4_stand_button.setObjectName("p4_stand_button")
            self.p4_stand_button.setText("STAND")
            self.p4_verticalLayout.addWidget(self.p4_stand_button)
            # PLAYER 4
            self.p4_exit_button = QtWidgets.QPushButton(self.p4_verticalLayoutWidget, clicked=lambda: self.exit_it())
            self.p4_exit_button.setObjectName("p4_exit_button")
            self.p4_exit_button.setText("EXIT")
            self.p4_verticalLayout.addWidget(self.p4_exit_button)

            self.your_cards_left_field.setPlainText(str(cards[1][0]))
            self.your_cards_right_field.setPlainText(str(cards[1][1]))
            self.amount_left_label.setText("Amount Left: " + str(amounts_list[1]))
            self.current_bet_field.setPlainText(str(self.player_bets[1]))

            self.p2_left_field.setPlainText(str(cards[2][0]))
            self.p2_right_field.setPlainText(str(cards[2][1]))
            self.p2_amount_left_label.setText("Amount Left: " + str(amounts_list[2]))
            self.p2_current_bet_field.setPlainText(str(self.player_bets[2]))

            self.p3_left_field.setPlainText(str(cards[3][0]))
            self.p3_right_field.setPlainText(str(cards[3][1]))
            self.p3_amount_left_label.setText("Amount Left: " + str(amounts_list[3]))
            self.p3_current_bet_field.setPlainText(str(self.player_bets[3]))

            self.p4_left_field.setPlainText(str(cards[4][0]))
            self.p4_right_field.setPlainText(str(cards[4][1]))
            self.p4_amount_left_label.setText("Amount Left: " + str(amounts_list[4]))
            self.p4_current_bet_field.setPlainText(str(self.player_bets[4]))           
        #
        #
        #########################################################################


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
        #self.amount_left_label.setText(_translate("MainWindow", "Amount Left: ") + str(amounts_list[1]))


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
        
        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(db.check)

        # just start one timer
        self.timer.start()
        
        print("entered init confirm_round...")


    # UPON CONFIRM BUTTON PRESS: CLOSE CURRENT GUIS, OPEN PLAYER_READY GUI
    def confirm_connection(self, prev_w):
        global button_counter
        print("entered confirmation button method...")

        
        self.timer.stop() # TESTING STOP TIMER
        hb.button_press.disconnect()
        db.button_press.disconnect()
        button_counter += 1 # changing state

        hb.button_press.connect(prev_w.hit_it)
        sb.button_press.connect(prev_w.stand_it)
        db.button_press.connect(prev_w.double_it)
        eb.button_press.connect(prev_w.exit_it)
        

        # need to add connections for other player buttons

    def accept_connection(self):
        print("completing round to BJ...")
        """
        msg = Message("complete_round", None)
        gui_to_bj_queue.put(msg)
        """


    # UPON CANCEL BUTTON PRESS: DO NOTHING
    def reject_connection(self):
        print("rejected the connection...")

    # STYLES/SETUP OF CONFIRM BOX GUI
    def setupUi(self, prev_w, confirm_round):
        prev_w_settings = prev_w
        confirm_round.setObjectName("confirm_round")
        confirm_round.resize(WIDTH, HEIGHT)

        # button styles/configurations
        self.buttonBox = QtWidgets.QDialogButtonBox(confirm_round)
        self.buttonBox.setGeometry(180, 260, 500, 200)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.confirm_connection(prev_w_settings))
        #self.buttonBox.rejected.connect(lambda: self.reject_connection())
        hb.button_press.connect(self.buttonBox.accepted)
        db.button_press.connect(self.buttonBox.rejected)
        #self.buttonBox.accepted.connect(self.accept_connection)
        self.buttonBox.rejected.connect(self.reject_connection)

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
        # testing button functionality for multiple function calls
        self.timer = QtCore.QTimer(interval=50)

        self.timer.timeout.connect(hb.check)
        self.timer.timeout.connect(db.check)

        # just start one timer
        self.timer.start()

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

        self.timer.stop()
        hb.button_press.disconnect()
        db.button_press.disconnect()

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
        hb.button_press.connect(self.buttonBox.accepted)
        db.button_press.connect(self.buttonBox.rejected)

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
