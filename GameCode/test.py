import RPi.GPIO as GPIO
from time import sleep

pin = 16
pin_list = [16,20,21] #GPIO pins to be used
GPIO.setmode(GPIO.BCM)

#initalize all pins in list as output and LOW
GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(16, GPIO.HIGH) #set as HIGH
GPIO.output(20, GPIO.HIGH)
GPIO.output(21, GPIO.HIGH)
print(GPIO.input(pin))
sleep(4)

GPIO.output(16, GPIO.LOW) #set as LOW
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
print(GPIO.input(pin))
sleep(1)

GPIO.cleanup() #reset pins

print("Done")

def shuffle():
    GPIO.output(21, 1)
    sleep(1)
    GPIO.output(21, 0)
