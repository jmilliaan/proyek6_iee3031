import cv2
from picamera.array import PiRGBArray as pi_rgb
from picamera import PiCamera as picam
from scipy.ndimage.filters import gaussian_filter
import time
import roboconvcv_constants as constants

class Frame:
    def __init__(self, frame):
        self.raw_frame = frame
        self.bw = cv2.cvtColor(self.raw_frame, cv2.COLOR_BGR2GRAY)
        self.canny_min = constants.cv_canny_min
        self.canny_max = constants.cv_canny_max
        self.sigma_val = 1
        self.blurred = self.blur(self.sigma_val)
        self.canny_edges = self.canny(self.blurred,
                                      self.canny_min,
                                      self.canny_max)
        self.cannydetector = []
        self.c_x = 0
        self.c_y = 0
        self.frame_magnitude = 0
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

    def centroid(self, img):
        self.frame_magnitude = cv2.sumElems(img)
        self.frame_moments = cv2.moments(img)
        if constants.cv_magnitude_lower_boundary < self.frame_magnitude < constants.cv_magnitude_upper_boundary:
            if self.frame_moments["m00"] != 0:
                self.c_x = int(self.frame_moments["m10"] / self.frame_moments["m00"])
                self.c_y = int(self.frame_moments["m01"] / self.frame_moments["m00"])
        return self.c_x, self.c_y


class PiCam:
    def __init__(self):
        self.cam = picam()
        self.cam.resolution = constants.cv_resolution
        self.cam.framerate = constants.cv_framerate
        self.raw_cap = pi_rgb(picam, size=self.cam.resolution)
        time.sleep(0.1)
