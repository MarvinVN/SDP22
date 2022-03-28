"""
        # clearing all widgets (necessary to avoid errors)
        for i in reversed(range(self.formLayout.count())): 
            self.formLayout.itemAt(i).widget().setParent(None)
"""


        # TODO: need to change this to be similar to below formatting (get rid of centralwidget, need formLayout)
        # set vertical box layout
        #self.centralwidget.setLayout(QtWidgets.QVBoxLayout())
        #self.betting_label = QtWidgets.QLabel("Betting for this round?")




"""
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

        sb.button_press.connect(lambda: self.openWindow(self.p1_mw))
"""
"""
        self.ready_pushButton.setFont(font16)
        self.ready_pushButton.setObjectName("ok_pushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ok_pushButton)
"""



"""
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

"""