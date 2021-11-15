from PyQt5 import QtCore, QtGui, QtWidgets
from jackblack_player1 import Ui_Player1_MainWindow


class Ui_confirm_dialogbox(object):
    def confirm_connection(self, set_w):
        # need to open new window and hide settings window
        #temp_w = setting_w
        set_w.hide()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Player1_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def reject_connection(self):
        pass

    def setupUi(self, confirm_dialogbox, SettingsWindow):
        confirm_dialogbox.setObjectName("confirm_dialogbox")
        confirm_dialogbox.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(confirm_dialogbox)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.confirm_connection(SettingsWindow))
        self.buttonBox.rejected.connect(lambda: self.reject_connection())

        self.widget = QtWidgets.QWidget(confirm_dialogbox)
        self.widget.setGeometry(QtCore.QRect(40, 10, 308, 228))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    confirm_dialogbox = QtWidgets.QDialog()
    ui = Ui_confirm_dialogbox()
    ui.setupUi(confirm_dialogbox)
    confirm_dialogbox.show()
    sys.exit(app.exec_())
