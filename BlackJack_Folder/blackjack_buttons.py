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