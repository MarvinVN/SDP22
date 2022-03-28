import RPi.GPIO as GPIO
from time import sleep

pin_list = [16,20,21] #GPIO pins to be used;
confirm_pin = 13 #for scan confirmation

states = {
    "idle": [0,0,0],
    "shuffler": [0,0,1],
    "init_deal": [0,1,0],
    "p1": [0,1,1],
    "p2": [1,0,0],
    "p3": [1,0,1],
    "p4": [1,1,0],
    "p5": [1,1,1]
}

#already called in blackjack.py; sets up GPIO
#GPIO.setmode(GPIO.BCM)

#already done in blackjack.py; initalize all pins in list as output and LOW
#GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

def scanConfirm():
    GPIO.output(confirm_pin, GPIO.HIGH)
    sleep(1)
    GPIO.output(confirm_pin, GPIO.LOW)

def signal(state):
    if state[0]:
        GPIO.output(21, GPIO.HIGH)
    if state[1]:
        GPIO.output(20, GPIO.HIGH)
    if state[2]:
        GPIO.output(16, GPIO.HIGH)

    sleep(1) #work on timing

    GPIO.output(pin_list, GPIO.LOW)

    sleep(1)

def shuffle():
    """GPIO.output(16, GPIO.HIGH)
    #GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(1)

    print("shuffle")

    GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    #GPIO.output(21, GPIO.LOW)
    sleep(1)  """

    signal(states["shuffler"])  #TODO: test this method with pi

def init_deal():
    """
    #GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(4)

    #GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    #GPIO.output(21, GPIO.LOW)
    sleep(1)"""

    print("initial deal")
    signal(states["init_deal"])    


def p1():
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(2)

    print("player one card")

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    #GPIO.output(21, GPIO.LOW)
    sleep(1)    

def p2():
    #GPIO.output(16, GPIO.HIGH)
    #GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(1)

    #GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    

def p3():
    GPIO.output(16, GPIO.HIGH)
    #GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    print("player three card")

    GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    

def p4():
    #GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    print("player four card")

    #GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    


def p5():
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    print("player five card")

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    

"""""
#GPIO.cleanup() #reset pins
#TEST-----

#already called in blackjack.py; sets up GPIO
GPIO.setmode(GPIO.BCM)

#already done in blackjack.py; initalize all pins in list as output and LOW
GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

init_deal()

GPIO.cleanup()
"""