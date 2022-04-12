import RPi.GPIO as GPIO
from time import sleep

pin_list = [16,20,21] #GPIO pins to be used;
confirm_pin = 13 #for scan confirmation

states = {
    "idle": [0,0,0],
    "p0": [0,0,1],
    "p1": [0,1,0],
    "p2": [0,1,1],
    "p3": [1,0,0],
    "p4": [1,0,1],
    "shuffler": [1,1,1]
}

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

    signal(states["shuffler"])
    sleep(1)

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


def p0():
    """"
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(2)

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    #GPIO.output(21, GPIO.LOW)
    sleep(1)"""

    print("dealer card")
    signal(states["p0"])

def p1():
    """
    #GPIO.output(16, GPIO.HIGH)
    #GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(1)

    #GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)"""

    print("player one card")
    signal(states["p1"])  

def p2():
    """
    GPIO.output(16, GPIO.HIGH)
    #GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    print("player three card")

    GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)"""

    print("player two card")
    signal(states["p2"]) 

def p3():
    """
    #GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    print("player four card")

    #GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)"""

    print("player three card")
    signal(states["p3"])


def p4():
    """
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    print("player five card")

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1) """

    print("player 4 card")
    signal(states["p4"]) 