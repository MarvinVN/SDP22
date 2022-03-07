from re import T
import RPi.GPIO as GPIO
from time import sleep

def hit(channel):
    print(f"button press {channel} detected, HIT")

def stand(channel):
    print(f"button press {channel} detected, STAND")

buttons = {
    "hit":19,
    "stand":26
}

GPIO.setmode(GPIO.BCM)

GPIO.setup(list(buttons.values()), GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.add_event_detect(buttons["hit"], GPIO.FALLING, callback=hit, bouncetime=300)
    GPIO.add_event_detect(buttons["stand"], GPIO.FALLING, callback=stand, bouncetime=300)
    while True:
        print("waiting")
        sleep(.5)    

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
