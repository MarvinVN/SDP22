import RPi.GPIO as GPIO
from time import sleep
import dealer

pin_list = [16,20,21] 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

print("Shuffling")
dealer.shuffle()

GPIO.cleanup()