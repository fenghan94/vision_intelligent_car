import time
import numpy as np
import pygame
import serial
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera


class CollectTrainingData(object):
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.send_inst = True

        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        self.pygame_init()

        self.collect_data()

    def pygame_init(self):
        pygame.init()
        display_size = (300, 400)
        screen = pygame.display.set_mode(display_size)
        background = pygame.Surface(screen.get_size())
        color_white = (255, 255, 255)
        display_font = pygame.font.Font(None, 40)
        pygame.display.set_caption('Control')
        text = display_font.render('Use arrows to move', 1, color_white)
        text_position = text.get_rect(centerx=display_size[0] / 2)
        background.blit(text, text_position)
        screen.blit(background, (0, 0))
        pygame.display.flip()

    def collect_data(self):
        saved_frame = 0
        total_frame = 0
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')
        frame_num = 1

        with PiCamera() as camera:
            # camera = PiCamera()
            camera.resolution = (320, 240)
            camera.framerate = 30
            rawCapture = PiRGBArray(camera, size=(320, 240))
            time.sleep(0.1)
            while self.send_inst:
                print "1"

                for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
                    print "2"
                    img = frame.array
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    roi = img[120:240, :]
                    success_write = cv2.imwrite('training_images/frame_num{:>05}.jpg'.format(frame_num), img)
                    # cv2.imshow('image', img)
                    print success_write
                    temp_array = roi.reshape(1, -1).astype(np.float32)
                    # print np.shape(temp_array)
                    frame_num += 1
                    total_frame += 1

                    for event in pygame.event.get():
                        print 3
                        if event.type == pygame.KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            if key_input[pygame.K_UP]:
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                self.ser.write(chr(119))

                            elif key_input[pygame.K_DOWN]:
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                self.ser.write(chr(115))

                            elif key_input[pygame.K_RIGHT]:
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.ser.write(chr(100))

                            elif key_input[pygame.K_LEFT]:
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.ser.write(chr(97))

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print "exit"
                                self.send_inst = False
                                self.ser.write(chr(113))
                                break

                        elif event.type == pygame.KEYUP:
                            self.ser.write(chr(113))
                    rawCapture.truncate(0)
            print "exit 1"
            train = image_array[1:, :]
            train_labels = label_array[1:, :]
            np.savez('training_data_temp/test01.npz', train=train, train_labels=train_labels)


if __name__ == '__main__':
    CollectTrainingData()
