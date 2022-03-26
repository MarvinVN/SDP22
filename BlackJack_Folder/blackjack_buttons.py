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

"""
# this main window class can be removed for final
# just need this for testing purposes right now
# move button calls into gui file
class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here
        self.widget = qtw.QWidget()
        self.widget.setLayout(qtw.QFormLayout())
        self.setCentralWidget(self.widget)
                        
        self.hit_button = HWButton(17)
        self.stand_button = HWButton(27)
        self.double_button = HWButton(22)
        self.exit_button = HWButton(23)

        self.hit_button.button_press.connect(self.testingHitButton)
        self.stand_button.button_press.connect(self.testingStandButton)
        self.double_button.button_press.connect(self.testingDoubleButton)
        self.exit_button.button_press.connect(self.testingExitButton)

        # End main UI code
        self.show()



    def testingHitButton(self):
        readbutton = qtw.QPushButton('HIT')
        self.widget.layout().addRow(readbutton)

    def testingStandButton(self):
        readbutton = qtw.QPushButton('STAND')
        self.widget.layout().addRow(readbutton)
    def testingDoubleButton(self):
        readbutton = qtw.QPushButton('DOUBLE')
        self.widget.layout().addRow(readbutton)
    def testingExitButton(self):
        readbutton = qtw.QPushButton('EXIT')
        self.widget.layout().addRow(readbutton)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
"""