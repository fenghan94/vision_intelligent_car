import picamera
import picamera.array
import time

with picamera.PiCamera() as camera:
    camera.resolution = (320,240)
    camera.framerate = 30
    print "start preview direct from GPU"
    camera.start_preview() # the start_preview() function   
    time.sleep(10)
    print "end preview"
