from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Player1_MainWindow(object):
    def bet_it(self):
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
        self.betting_label.setGeometry(QtCore.QRect(170, 60, 291, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.betting_label.setFont(font)
        self.betting_label.setAcceptDrops(False)
        self.betting_label.setAlignment(QtCore.Qt.AlignCenter)
        self.betting_label.setObjectName("betting_label")

        # betting amount
        self.scroll_bet = QtWidgets.QSpinBox(self.centralwidget,
            maximum=500,
            minimum=10,
            value=10,
            singleStep=10)
        self.scroll_bet.setGeometry(QtCore.QRect(160, 160, 311, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.scroll_bet.setFont(font)
        self.scroll_bet.setObjectName("scroll_bet")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.scroll_bet)

        # ok button
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.ok_it())
        self.ok_pushButton.setText("OK")
        self.ok_pushButton.setGeometry(QtCore.QRect(160, 160, 311, 61))
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


    def ok_it(self):
        for i in reversed(range(self.formLayoutWidget.layout().count())): 
            self.formLayoutWidget.layout().itemAt(i).widget().deleteLater()

        self.test_label = QtWidgets.QLabel("YAYYYYY")
        self.formLayoutWidget.layout().addWidget(self.test_label)



    def setupUi(self, Player1_MainWindow):
        Player1_MainWindow.setObjectName("Player1_MainWindow")
        Player1_MainWindow.resize(610, 368)
        self.centralwidget = QtWidgets.QWidget(Player1_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # making a form layout
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(160, 150, 381, 214))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.player1_label = QtWidgets.QLabel(self.centralwidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.player1_label)
        self.player1_label.setGeometry(QtCore.QRect(170, 60, 291, 71))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.player1_label.setFont(font)
        self.player1_label.setAcceptDrops(False)
        self.player1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.player1_label.setObjectName("player1_label")


        self.ready_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.bet_it())
        self.ready_pushButton.setGeometry(QtCore.QRect(170, 160, 291, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ready_pushButton.setFont(font)
        self.ready_pushButton.setObjectName("ready_pushButton")
        #self.ready_pushButton.setAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ready_pushButton)
        Player1_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Player1_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 610, 22))
        self.menubar.setObjectName("menubar")
        Player1_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Player1_MainWindow)
        self.statusbar.setObjectName("statusbar")
        Player1_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(Player1_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Player1_MainWindow)

    def retranslateUi(self, Player1_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Player1_MainWindow.setWindowTitle(_translate("Player1_MainWindow", "Player1"))
        self.player1_label.setText(_translate("Player1_MainWindow", "Player 1"))
        #self.betting_label.setText(_translate("Player1_MainWindow", "Betting for this round?"))
        self.ready_pushButton.setText(_translate("Player1_MainWindow", "PRESS HERE WHEN READY!"))
        #self.ok_pushButton.setText(_translate("Player1_MainWindow", "OK"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Player1_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Player1_MainWindow()
    ui.setupUi(Player1_MainWindow)
    Player1_MainWindow.show()
    sys.exit(app.exec_())
