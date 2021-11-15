from PyQt5 import QtCore, QtGui, QtWidgets

# maybe add a struct for Player information?
class Ui_MainWindow(object):
    # when the "DOUBLE" button is pressed, update the value of current bet, display update
    def double_it(self):
        value = self.current_bet_field.toPlainText()
        value = int(value) * 2
        self.current_bet_field.setPlainText(str(value))

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
        MainWindow.resize(480, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(150, 180, 160, 80))
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
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(150, 10, 160, 80))
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
        self.current_bet_field.setGeometry(QtCore.QRect(20, 180, 81, 81))
        self.current_bet_field.setObjectName("current_bet_field")

        self.amount_left_label = QtWidgets.QLabel(self.centralwidget)
        self.amount_left_label.setGeometry(QtCore.QRect(380, 10, 91, 20))
        self.amount_left_label.setObjectName("amount_left_label")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(370, 170, 91, 91))
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 160, 61, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 100, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 160, 71, 20))
        self.label_3.setObjectName("label_3")
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
        self.amount_left_label.setText(_translate("MainWindow", "Amount Left: "))
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
