# new file with the GUI classes
from PyQt5 import QtCore, QtGui, QtWidgets
import blackjack

HEIGHT = 480
WIDTH = 800

# touch display 3.5 inch: 320x480 res

###########################################################
#################### MAIN WINDOW CLASS ####################
###########################################################


class Ui_MainWindow(object):

    def __init__(self):
        pass

    def mainToSettings(self, current_w):
        temp_w = current_w
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        temp_w.hide()


    def setupUi(self, MainWindow):
        self.width = WIDTH
        self.height = HEIGHT
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(320, 480)
        MainWindow.resize(self.width, self.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.mainToSettings(MainWindow))
        # setGeometry(left, top, width, height)
        #self.pushButton.setGeometry(QtCore.QRect(190, 280, 421, 141))
        self.pushButton.setGeometry(240, 300, 310, 50)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        #self.label.setGeometry(QtCore.QRect(190, 140, 421, 111))
        self.label.setGeometry(220, 200, 360, 70)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
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
        self.pushButton.setText(_translate("MainWindow", "Start Game"))
        self.label.setText(_translate("MainWindow", "JACKBLACK"))


###########################################################
#################### SETTINGS WINDOW CLASS ################
###########################################################


class Ui_SettingsWindow(object):

    def __init__(self):
        self.numPlayers = "0"
        self.startingAmount = 0
        # change these eventually
        self.gameMode = ""
        self.userInput = ""

    def openWindow(self, settings_w):
        # storing the setting values into variables
        self.numPlayers = self.numberOfPlayersComboBox.currentText()
        self.startingAmount = self.startingAmountSpinBox.value()
        self.gameMode = self.gameModeSelect1ComboBox.currentText()
        self.userInput = self.insert.text()

        # opening up the confirmation box with user-selected settings
        self.window = QtWidgets.QDialog()
        self.ui = Ui_confirm_dialogbox(self.numPlayers, self.startingAmount, self.gameMode, self.userInput)
        self.ui.setupUi(self.window, settings_w)

        # displaying the values onto confirmation box
        self.ui.confirm_list_widget.addItems(["Number of Players: " + self.numPlayers,
            "Starting Amount: " + str(self.startingAmount),
            "Game Mode: " + self.gameMode,
            "User Input: " + self.userInput])
        self.window.show()

    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(WIDTH, HEIGHT)
        font = QtGui.QFont()
        font.setPointSize(12)
        SettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(300, 50, 360, 70)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(180, 130, 500, 200)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
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
        self.gameModeSelect1Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.gameModeSelect1Label.setObjectName("gameModeSelect1Label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.gameModeSelect1Label)
        self.gameModeSelect1ComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.gameModeSelect1ComboBox.addItems(["Winning Amount", "Number of Wins", "Total Games", "Duration"])
        self.gameModeSelect1ComboBox.setObjectName("gameModeSelect1ComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gameModeSelect1ComboBox)
        self.insertLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.insertLabel.setObjectName("insertLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.insertLabel)
        self.insert = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.insert.setObjectName("insert")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.insert)
        self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget, clicked=lambda: self.openWindow(SettingsWindow))
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pushButton)
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 38))
        self.menubar.setObjectName("menubar")
        SettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
        self.statusbar.setObjectName("statusbar")
        SettingsWindow.setStatusBar(self.statusbar)
        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
        self.label.setText(_translate("SettingsWindow", "Game Play Settings"))
        self.numberOfPlayersLabel.setText(_translate("SettingsWindow", "Number of Players:"))
        self.numberOfPlayersComboBox.setItemText(0, _translate("SettingsWindow", "1"))
        self.numberOfPlayersComboBox.setItemText(1, _translate("SettingsWindow", "2"))
        self.numberOfPlayersComboBox.setItemText(2, _translate("SettingsWindow", "3"))
        self.numberOfPlayersComboBox.setItemText(3, _translate("SettingsWindow", "4"))
        self.startingAmountLabel.setText(_translate("SettingsWindow", "Starting Amount:"))
        self.gameModeSelect1Label.setText(_translate("SettingsWindow", "Game Mode (select 1):"))
        self.insertLabel.setText(_translate("SettingsWindow", "User Input:"))
        self.pushButton.setText(_translate("SettingsWindow", "CONTINUE"))


###########################################################
#################### CONFIRM BOX CLASS ####################
###########################################################


class Ui_confirm_dialogbox(object):

    def __init__(self, numPlayers, startingAmount, gameMode, userInput):
        self.numPlayers = numPlayers
        self.startingAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput

    def confirm_connection(self, set_w):
        # need to open new window and hide settings window
        #temp_w = setting_w
        set_w.hide()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Player_ReadyWindow(self.numPlayers, self.startingAmount, self.gameMode, self.userInput)
        self.ui.setupUi(self.window)
        self.window.show()

    def reject_connection(self):
        pass

    def setupUi(self, confirm_dialogbox, SettingsWindow):
        confirm_dialogbox.setObjectName("confirm_dialogbox")
        confirm_dialogbox.resize(WIDTH, HEIGHT)
        self.buttonBox = QtWidgets.QDialogButtonBox(confirm_dialogbox)
        self.buttonBox.setGeometry(180, 260, 500, 200)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.confirm_connection(SettingsWindow))
        self.buttonBox.rejected.connect(lambda: self.reject_connection())

        self.widget = QtWidgets.QWidget(confirm_dialogbox)
        self.widget.setGeometry(180, 100, 500, 200)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.confirm_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confirm_label.setFont(font)
        self.confirm_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.confirm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.confirm_label.setObjectName("confirm_label")
        self.verticalLayout.addWidget(self.confirm_label)
        self.confirm_list_widget = QtWidgets.QListWidget(self.widget)
        self.confirm_list_widget.setObjectName("confirm_list_widget")
        self.verticalLayout.addWidget(self.confirm_list_widget)

        self.retranslateUi(confirm_dialogbox)
        self.buttonBox.accepted.connect(confirm_dialogbox.accept)
        self.buttonBox.rejected.connect(confirm_dialogbox.reject)
        QtCore.QMetaObject.connectSlotsByName(confirm_dialogbox)

    def retranslateUi(self, confirm_dialogbox):
        _translate = QtCore.QCoreApplication.translate
        confirm_dialogbox.setWindowTitle(_translate("confirm_dialogbox", "Confirmation"))
        self.confirm_label.setText(_translate("confirm_dialogbox", "Are these configurations correct?"))


###########################################################
#################### PLAYER READY CLASS ####################
###########################################################

class Ui_Player_ReadyWindow(object):

    def __init__(self, numPlayers, startingAmount, gameMode, userInput):
        self.numPlayers = numPlayers
        self.startingAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput
        self.bet = 0

    def bet_it(self, p1_mw):
        for i in reversed(range(self.formLayout.count())): 
            self.formLayout.itemAt(i).widget().setParent(None)

        # need to change this to be similar to below formatting (get rid of centralwidget, need formLayout)
        # set vertical box layout
        #self.centralwidget.setLayout(QtWidgets.QVBoxLayout())
        #self.betting_label = QtWidgets.QLabel("Betting for this round?")

        # betting label
        self.betting_label = QtWidgets.QLabel(self.centralwidget)
        self.betting_label.setText("Betting for this round?")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.betting_label)
        self.betting_label.setGeometry(180, 100, 500, 200)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.betting_label.setFont(font)
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
        font = QtGui.QFont()
        font.setPointSize(16)
        self.scroll_bet.setFont(font)
        self.scroll_bet.setObjectName("scroll_bet")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.scroll_bet)

        # ok button
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openWindow(p1_mw))
        self.ok_pushButton.setText("OK")
        self.ok_pushButton.setGeometry(180, 170, 500, 200)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ready_pushButton.setFont(font)
        self.ready_pushButton.setObjectName("ok_pushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ok_pushButton)

        # change the font and size of label
        #self.betting_label.setFont(QtGui.QFont('Helvetica', 24))
        #self.centralwidget.layout().addWidget(self.betting_label)
        """
        self.hbox = QtWidgets.QHBoxLayout()
        self.scroll_bet = QtWidgets.QSpinBox(self.centralwidget,
            maximum=500,
            minimum=10,
            value=10,
            singleStep=10)
        self.hbox.addWidget(self.scroll_bet)
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(lambda: self.ok_it())
        self.hbox.addWidget(self.ok_button)
        self.centralwidget.layout().addLayout(self.hbox)
        """
    # def double_it(self):
    #     #self.display_bet = self.display_bet * 2
    #     self.bet = self.bet * 2
    #     self.ui.current_bet_field.setPlainText(str(self.bet))

    def openWindow(self, main_w):
        # open new window for game play GUI
        temp_w = main_w
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GameWindow(self.numPlayers, self.startingAmount, self.gameMode, self.userInput, self.bet)
        self.ui.setupUi(self.window)
        self.window.show()
        # below code runs infinite loop
        # this next line of code would be the start of a new event
        # blackjack.start_game(self.numPlayers, self.startingAmount, self.bet)

        # 

        # self.ui.current_bet_field.setPlainText(str(temp_w.scroll_bet.value))

        # displaying the betting amount
        self.bet = self.scroll_bet.value()
        #self.display_bet = self.bet
        self.ui.current_bet_field.setPlainText(str(self.bet))
        temp_w.hide()
        #self.ui.double_button.clicked.connect(double_it())


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

        self.player_label = QtWidgets.QLabel(self.centralwidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.player_label)
        #self.player1_label.setGeometry(170, 60, 291, 71)
        font = QtGui.QFont()
        font.setPointSize(48)
        self.player_label.setFont(font)
        self.player_label.setAcceptDrops(False)
        self.player_label.setAlignment(QtCore.Qt.AlignCenter)
        self.player_label.setObjectName("player_label")


        self.ready_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.bet_it(Player_ReadyWindow))
        self.ready_pushButton.setGeometry(100, 160, 250, 61)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ready_pushButton.setFont(font)
        self.ready_pushButton.setObjectName("ready_pushButton")
        #self.ready_pushButton.setAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ready_pushButton)
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

    def retranslateUi(self, Player_ReadyWindow):
        _translate = QtCore.QCoreApplication.translate
        Player_ReadyWindow.setWindowTitle(_translate("Player_ReadyWindow", "Player 1"))
        self.player_label.setText(_translate("Player_ReadyWindow", "Player 1"))
        #self.betting_label.setText(_translate("Player1_MainWindow", "Betting for this round?"))
        self.ready_pushButton.setText(_translate("Player_ReadyWindow", "PRESS HERE WHEN READY!"))
        #self.ok_pushButton.setText(_translate("Player1_MainWindow", "OK"))


###########################################################
#################### PLAYER GAME CLASS ####################
###########################################################

class Ui_GameWindow(object):

    def __init__(self, numPlayers, startingAmount, gameMode, userInput, bet):
        self.numPlayers = numPlayers
        self.currentAmount = startingAmount
        self.gameMode = gameMode
        self.userInput = userInput
        self.bet = bet
        self.double_button_clicked = False

    # when the "DOUBLE" button is pressed, update the value of current bet, display update
    def double_it(self):
        if self.double_button_clicked:
            pass
        else:
            value = self.current_bet_field.toPlainText()
            value = int(value) * 2
            self.current_bet_field.setPlainText(str(value))
            self.bet = value
            # this code below is to test whether the self.bet is updated properly
            #self.dealer_left_field.setPlainText(str(self.currentAmount))

        self.double_button_clicked = True
        # self.bet = self.bet * 2
        # self.current_bet_field.setPlainText(str(self.bet))

    # when "STAND" button is pressed, do nothing to current bet, do nothing to cards, reveal dealer cards
    def stand_it(self):
        pass

    # when "HIT" button is pressed, do nothing to current bet, add another card to player
    def hit_it(self):
        pass

    # display cards dealt to the player, save card information
    def player_cards(self):
        pass

    # deal cards to dealer, save card information, hide cards until STAND is pressed
    def dealer_cards(self):
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
        self.your_cards_layout.addWidget(self.your_cards_left_field)
        self.your_cards_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget,
            readOnly=True)
        self.your_cards_right_field.setObjectName("your_cards_right_field")
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
        self.dealer_cards_layout.addWidget(self.dealer_left_field)
        self.dealer_right_field = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2,
            readOnly=True)
        self.dealer_right_field.setObjectName("dealer_right_field")
        self.dealer_cards_layout.addWidget(self.dealer_right_field)

        self.current_bet_field = QtWidgets.QPlainTextEdit(self.centralwidget,
            readOnly=True)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.current_bet_field.setFont(font)
        self.current_bet_field.setGeometry(100, 310, 110, 110)
        self.current_bet_field.setObjectName("current_bet_field")

        # creating the amount left label
        font.setPointSize(10)
        self.amount_left_label = QtWidgets.QLabel(self.centralwidget)
        self.amount_left_label.setFont(font)
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

        # change font size to be a lot bigger; maybe size 10?
        font.setPointSize(10)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(355, 200, 110, 110)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(355, 140, 140, 110)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(110, 230, 110, 110)
        self.label_3.setObjectName("label_3")
        self.label.setFont(font)
        self.label_2.setFont(font)
        self.label_3.setFont(font)

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
        self.label.setText(_translate("MainWindow", "Your Cards:"))
        self.label_2.setText(_translate("MainWindow", "Dealer\'s Cards:"))
        self.label_3.setText(_translate("MainWindow", "Current Bet:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
