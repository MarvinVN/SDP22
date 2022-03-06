import RPi.GPIO as GPIO

p1_hit = 17
p1_stand = 27
p1_double = 22
p1_exit = 23
p1_buttons = [p1_hit, p1_stand, p1_double, p1_exit]

p2_hit = 5
p2_stand = 6
p2_double = 26
p2_exit = 16
p2_buttons = [p2_hit, p2_stand, p2_double, p2_exit]

def initGPIO():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(p1_buttons, GPIO.IN)
	GPIO.setup(p2_buttons, GPIO.IN)
