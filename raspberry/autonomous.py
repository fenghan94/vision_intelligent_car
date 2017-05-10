#!/usr/bin/python
import serial
import cv2
import numpy as np
import picamera
import time
import io


class NeuralNetwork(object):
    def __init__(self):
        self.model = cv2.ANN_MLP()

    def create(self):
        layer_size = np.int32([38400, 32, 4])
        self.model.create(layer_size)
        self.model.load('mlp_xml/mlp.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)


class Control(object):
    def __init__(self):
        self.serial_port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    def steer(self, prediction):
        if prediction == 2:
            self.serial_port.write(chr(119))
        elif prediction == 0:
            self.serial_port.write(chr(97))
        elif prediction == 1:
            self.serial_port.write(chr(100))
        else:
            self.stop()

    def stop(self):
        self.serial_port.write(chr(113))


def autonomous_control():
    model = NeuralNetwork()
    model.create()
    car = Control()

    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 30
        time.sleep(0.1)
        while True:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)
            gray = cv2.imdecode(np.fromstring(stream.getvalue(), dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
            half_gray = gray[120:240, :]
            image_array = half_gray.reshape(1, 38400).astype(np.float32)
            prediction = model.predict(image_array)
            stream.flush()
            car.steer(prediction)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                car.stop()
                break

if __name__ == '__main__':
    autonomous_control()
