import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

class HWButton(qtc.QObject):

    button_press = qtc.pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pressed = GPIO.input(self.pin) == GPIO.LOW

        self.timer = qtc.QTimer(interval=50, timeout=self.check)
        self.timer.start()

    def check(self):
        pressed = GPIO.input(self.pin) == GPIO.LOW
        if pressed != self.pressed:
            if pressed:
                self.button_press.emit()
            self.pressed = pressed


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here
        widget = qtw.QWidget()
        widget.setLayout(qtw.QFormLayout())
        self.setCentralWidget(widget)

        p = widget.palette()
        p.setColor(qtg.QPalette.WindowText, qtg.QColor('cyan'))
        p.setColor(qtg.QPalette.Window, qtg.QColor('navy'))
        p.setColor(qtg.QPalette.Button, qtg.QColor('#335'))
        p.setColor(qtg.QPalette.ButtonText, qtg.QColor('cyan'))
        self.setPalette(p)

        """
        butts = qtw.QMessageBox.about(self, "Testing", "Random Display for Buttons!")
        widget.layout().addRow('butts', butts)
        """
                        
        self.hwbutton = HWButton(8)
        self.hwbutton_thread = qtc.QThread()
        self.hwbutton.moveToThread(self.hwbutton_thread)
        self.hwbutton_thread.start()

        self.hwbutton.button_press.connect(self.testingButton)

        # End main UI code
        self.show()



    def testingButton(self):
        readbutton = qtw.QPushButton('Read Now')
        widget.layout().addRow(readbutton)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())