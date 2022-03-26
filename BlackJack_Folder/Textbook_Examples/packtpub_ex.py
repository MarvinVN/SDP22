from RPi import GPIO




class ThreeColorLed():
    """Represents a three color LED circuit"""

    def __init__(self, red, green, blue, pinmode=GPIO.BOARD, freq=50):
        GPIO.setmode(pinmode)

        self.pins = {
            "red": red,
            "green": green,
            "blue": blue
            }
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
        # Turn all on and all off
        for pin in self.pins.values():
            GPIO.output(pin, GPIO.HIGH)
            GPIO.output(pin, GPIO.LOW)

        self.pwms = dict([
             (name, GPIO.PWM(pin, freq))
             for name, pin in self.pins.items()
            ])
        for pwm in self.pwms.values():
            pwm.start(0)

    @staticmethod
    def convert(val):
        val = abs(val)
        val = val//2.55
        val %= 101
        return val

    def set_color(self, red, green, blue):
        """Set color using RGB color values of 0-255"""
        self.pwms['red'].ChangeDutyCycle(self.convert(red))
        self.pwms['green'].ChangeDutyCycle(self.convert(green))
        self.pwms['blue'].ChangeDutyCycle(self.convert(blue))

    def cleanup(self):
        GPIO.cleanup()

