import cv2
from picamera.array import PiRGBArray as pi_rgb
from picamera import PiCamera as picam
from scipy.ndimage.filters import gaussian_filter
import time
import numpy as np
import roboconvcv_constants as constants


class Frame:
    def __init__(self, frame):
        self.raw_frame = frame
        self.bw = cv2.cvtColor(self.raw_frame, cv2.COLOR_BGR2GRAY)
        self.canny_min = constants.cv_canny_min
        self.canny_max = constants.cv_canny_max
        self.sigma_val = 1.5
        self.blurred = self.blur(self.sigma_val)
        self.canny_edges = self.canny(self.blurred,
                                      self.canny_min,
                                      self.canny_max)
        self.c_x = 0
        self.c_y = 0
        self.cannydetector = []
        # self.frame_magnitude = 0
        self.frame_moments = 0

    def blur(self, sigma_val):
        blurred = gaussian_filter(self.bw, sigma=sigma_val)
        return blurred

    def canny(self, img, minval, maxval):
        cannydetector = cv2.Canny(img, minval, maxval)
        self.cannydetector = cannydetector
        return cannydetector

    def canny_difference(self, prev_frame):
        diff = cv2.subtract(self.blurred, prev_frame.blurred)
        return self.canny(diff, self.canny_min, self.canny_max)
        # return diff

    @staticmethod
    def fast_sum_image(src):
        return np.sum(src)

    def centroid(self, img):
        self.frame_moments = cv2.moments(img)
        new_x, new_y = 0, 0
        if self.frame_moments["m00"] != 0:
            new_x = int(self.frame_moments["m10"] / self.frame_moments["m00"])
            new_y = int(self.frame_moments["m01"] / self.frame_moments["m00"])
            self.c_x = new_x
            self.c_y = new_y
        return new_x, new_y


class PiCam:
    def __init__(self):
        self.cam = picam()
        self.cam.resolution = constants.cv_resolution
        self.cam.framerate = constants.cv_framerate
        self.raw_cap = pi_rgb(picam, size=self.cam.resolution)
        time.sleep(0.1)
