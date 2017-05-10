from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

traffic_cascade = cv2.CascadeClassifier('data.xml')

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320, 240))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    traffic = traffic_cascade.detectMultiScale(gray)

    for (x, y, w, h) in traffic:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    rawCapture.truncate(0)
    if k == 27:
        break

cv2.destroyAllWindows()
