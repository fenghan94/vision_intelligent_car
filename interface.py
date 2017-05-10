#!/usr/bin/python
# http://blog.csdn.net/bush2582/article/details/41308515?utm_source=tuicool&utm_medium=referral
from matplotlib import pyplot as plt
from matplotlib import animation
import urllib


f = plt.figure()
a = f.add_subplot(121)
b = f.add_subplot(122)
line1, = a.plot([], [], lw=2)
line2, = a.plot([], [], lw=2)
line3, = b.plot([], [], lw=2)


def read_values():
    link = "http://10.42.0.44:8080"
    date_list = []
    x_angle_list = []
    y_angle_list = []
    distance_list = []
    for i in range(20):
        data = urllib.urlopen(link)
        my_file = data.read()
        values = my_file.split(" ")
        date_list.append(values[0])
        x_angle_list.append(values[1])
        y_angle_list.append(values[2])
        distance_list.append(values[3])
    return date_list, x_angle_list, y_angle_list, date_list


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3


def animate(i):
    date, x_angle, y_angle, distance = read_values()
    line1.set_data(date, x_angle)
    line2.set_data(date, y_angle)
    line3.set_data(date, distance)
    return line1, line2, line3


ani = animation.FuncAnimation(f, animate, init_func=init, frames=50, interval=1000)
plt.show()
