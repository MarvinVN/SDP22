import time #time library to be able setup lenght of led lighting
import serial

#board = Arduino(Arduino.AUTODETECT) #detect Arduino with Autodetect
port = '/dev/cu.usbserial-1410'
x = '0'
baudrate = 115200
ser = serial.Serial(port,baudrate,timeout=1)

time.sleep(2)
ser.write(bytes(x, 'utf-8'))




