import serial, sys

def RFID():
    port = '/dev/cu.usbserial-1410'
    baudrate = 115200
    ser = serial.Serial(port,baudrate,timeout=1)
    data = ''
    while len(data) < 1:
        try:
            data = ser.readline().decode()
        except:
            print("Error")
        print(data)
    return data

