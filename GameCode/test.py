import RPi.GPIO as GPIO
from time import sleep

sleep(2)

pin_list = [16,20,21] #GPIO pins to be used
GPIO.setmode(GPIO.BCM)

#initalize all pins in list as output and LOW
GPIO.setup(pin_list, GPIO.OUT, initial=0)

GPIO.output(16, 1) #set 21 as HIGH
sleep(1)
GPIO.output(16, 0) #set 21 as LOW
sleep(1)

GPIO.cleanup() #reset pins

print("Done")

def shuffle():
    GPIO.output(21, 1)
    sleep(1)
    GPIO.output(21, 0)
