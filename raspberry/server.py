#!/usr/bin/python
import web
import smbus
import math
import time
import RPi.GPIO as GPIO

urls = (
    '/', 'index'
)

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)
address = 0x68

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.IN)

now = time.time()

def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def get_dist():
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(22, GPIO.LOW)
    while not GPIO.input(23):
        pass
    t1 = time.time()
    while GPIO.input(23):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 / 2


class index:
    def GET(self):
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        rotation_x = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        rotation_y = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

        distance = get_dist()

        return "{0:.4f} {1:.2f} {2:.2f} {3:.2f}".format(time.time() - now, rotation_x, rotation_y, distance)


if __name__ == "__main__":
    bus.write_byte_data(address, power_mgmt_1, 0)
    app = web.application(urls, globals())
    app.run()
    if KeyboardInterrupt:
        GPIO.cleanup()
