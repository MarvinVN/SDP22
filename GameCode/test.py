import RPi.GPIO as GPIO
from time import sleep

pin = 16
pin_list = [16,20,21] #GPIO pins to be used

states = {
    "idle": [0,0,0],
    "shuffler": [0,0,1],
    "motor-init": [0,1,0],
    "p1": [0,1,1],
    "p2": [1,0,0],
    "p3": [1,0,1],
    "p4": [1,1,0],
    "p5": [1,1,1]
}

#already called in  blackjack
#GPIO.setmode(GPIO.BCM)

#initalize all pins in list as output and LOW
#GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

def shuffle():
    GPIO.output(16, GPIO.HIGH)
    #GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(1)

    GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    #GPIO.output(21, GPIO.LOW)
    sleep(1)    

def init_deal():
    #GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(4)

    #GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    #GPIO.output(21, GPIO.LOW)
    sleep(1)    


def p1():
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    #GPIO.output(21, GPIO.HIGH)
    sleep(2)

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

    GPIO.output(16, GPIO.LOW)
    #GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    

def p4():
    #GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    #GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    


def p5():
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    sleep(4)

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    sleep(1)    

#GPIO.cleanup() #reset pins