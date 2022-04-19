import RPi.GPIO as GPIO
from time import sleep

from numpy import True_
import dealer
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([16,20,21], GPIO.OUT, initial=GPIO.LOW)

    rfid()

    GPIO.cleanup()

def buttons():
    player_buttons = {
    1: {"hit": 2, "stand": 3, "double": 4},
    2: {"hit": 14, "stand": 15, "double": 18},
    3: {"hit": 17, "stand": 27, "double": 22},
    4: {"hit": 23, "stand": 24, "double": 25}
    }

    pins = [x for pins in player_buttons.values() for x in pins.values()]

    GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(pins)

    for x in pins: GPIO.add_event_detect(x, GPIO.FALLING, bouncetime=100)
    try:
        while True:
            sleep(.1)
            if GPIO.event_detected(2):
                print("p1 hit")
            if GPIO.event_detected(3):
                print("p1 stand")
            if GPIO.event_detected(4):
                print("p1 doub")
            if GPIO.event_detected(14):
                print("p2 hit")
            if GPIO.event_detected(15):
                print("p2 stand")
            if GPIO.event_detected(18):
                print("p2 doub")
            if GPIO.event_detected(17):
                print("p3 hit")
            if GPIO.event_detected(27):
                print("p3 stand")
            if GPIO.event_detected(22):
                print("p3 doub")      
            if GPIO.event_detected(23):
                print("p4 hit")      
            if GPIO.event_detected(24):
                print("p4 stand")     
            if GPIO.event_detected(25):
                print("p4 doub")                   
    except KeyboardInterrupt:
        for x in pins: GPIO.remove_event_detect(x)
        GPIO.cleanup()
            


def rfid():
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)
    pn532.SAM_configuration()

    print("Waiting for card...")
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is None:
            continue
        card = [hex(i) for i in uid]
        break
    print(card)

def shuffle():
    dealer.shuffle()

if __name__ == "__main__":
    main() 