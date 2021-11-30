import cv2
from scipy.ndimage.filters import gaussian_filter, convolve
import numpy as np


class Frame:
    def __init__(self, frame):
        self.raw_frame = frame
        self.bw = cv2.cvtColor(self.raw_frame, cv2.COLOR_BGR2GRAY)

    def blur(self, sigma_val):
        blurred = gaussian_filter(self.bw, sigma=1)
        return blurred

    def canny(self, minval, maxval):
        cannydetector = cv2.Canny(self.blur, minval, maxval)
        return cannydetector
