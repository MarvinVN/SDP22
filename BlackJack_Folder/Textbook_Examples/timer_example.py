import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
from PyQt5.QtCore import QTimer,QDateTime
import gpio_example

class WinForm(QWidget):
    def __init__(self,parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('QTimer example')

        self.variable = 0

        self.listFile=QListWidget()
        self.label=QLabel('Label')
        self.startBtn=QPushButton('Start')
        self.endBtn=QPushButton('Stop')

        layout=QGridLayout()

        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)


        layout.addWidget(self.label,0,0,1,2)
        layout.addWidget(self.startBtn,1,0)
        layout.addWidget(self.endBtn,1,1)

        # testing gpio
        #self.gpioTest()
        # if the .connect does not work, put this into the timer function to manually check if statement every 10 ms
        self.p1_hit_button.is_pressed.connect(self.eventDetected)

        # these ones would be changed to the gui game start trigger
        # once game starts, interrupt Timer starts and constantly interrupt to check gpio input signal
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        self.endBtn.clicked.connect(self.eventDetected)

        self.setLayout(layout)

    def showTime(self):
        time=QDateTime.currentDateTime()
        self.variable = self.variable+1
        # for each button, read button and save to local variable
        # state of game, state of buttons
        # draw diagram of the state of the game
        # get timer part working first
        # get buttons working, then combine piece by piece
        # go function by function

        # in this function, instead of printing out every interrupt, want to check if a signal has been sent from gpio
        timeDisplay="Interrupt #: " + str(self.variable)
        self.label.setText(timeDisplay)

    # detect an event signal
    def eventDetected(self):
        eventDisplay = "An event was detected!"
        self.label.setText(eventDisplay)

    def startTimer(self):
        self.timer.start(10)
        # might need to move the button clicked checking here
        # I can use these to set the GUI buttons to clicked/not clicked
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=WinForm()
    form.show()
    sys.exit(app.exec_())