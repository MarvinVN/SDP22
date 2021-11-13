
import serial, sys
port = '/dev/cu.usbserial-1410'
baudrate = 115200
ser = serial.Serial(port,baudrate,timeout=1)
while True:
    data = ser.readline().decode()
    print(data)
    data = ''