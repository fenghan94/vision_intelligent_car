import serial
import binascii
ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)

# a=binascii.b2a_hex('A')
# print(a)
ser.write(hex(65))
ser.close()
