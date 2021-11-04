from PyQt5 import QtCore, QtGui, QtWidgets
from jackblack_confirm_box import Ui_confirm_dialogbox


class Ui_SettingsWindow(object):
    def openWindow(self, settings_w):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_confirm_dialogbox()
        self.ui.setupUi(self.window, settings_w)
        self.ui.confirm_list_widget.addItems(["Number of Players: " + self.numberOfPlayersComboBox.currentText(),
            "Starting Amount: " + str(self.startingAmountSpinBox.value()),
            "Game Mode: " + self.gameModeSelect1ComboBox.currentText(),
            "User Input: " + self.insert.text()])
        self.window.show()

    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(716, 533)
        font = QtGui.QFont()
        font.setPointSize(12)
        SettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 40, 421, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(160, 150, 381, 214))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.numberOfPlayersLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.numberOfPlayersLabel.setObjectName("numberOfPlayersLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.numberOfPlayersLabel)
        self.numberOfPlayersComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.numberOfPlayersComboBox.setObjectName("numberOfPlayersComboBox")
        #font2 = QtGui.QFont()
       # font2.setPointSize(24)
        #self.numberOfPlayersComboBox.setFont(font2)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QMainWindow()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())
