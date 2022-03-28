"""
        # clearing all widgets (necessary to avoid errors)
        for i in reversed(range(self.formLayout.count())): 
            self.formLayout.itemAt(i).widget().setParent(None)
"""


        # TODO: need to change this to be similar to below formatting (get rid of centralwidget, need formLayout)
        # set vertical box layout
        #self.centralwidget.setLayout(QtWidgets.QVBoxLayout())
        #self.betting_label = QtWidgets.QLabel("Betting for this round?")
