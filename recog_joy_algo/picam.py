from picamera.array import PiRGBArray
from picamera import PiCamera
from capture_class import Frame
import cv2
import time
import RPi.GPIO as GPIO
from mysql_proyek6 import DBConnection
import ssc32
import constants

dbconn = DBConnection()

username = "jm03"
password = "191900103"
topic = "channel"

broker_ip = "10.252.243.158"

mode = 1

ch1_prev = 0
ch2_prev = 0
ch3_prev = 0
ch4_prev = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

controlpin = 14

GPIO.setup(controlpin, GPIO.OUT)
pwm = GPIO.PWM(controlpin, 100)

dc = 90

frame_count = 0
reset_count = 0

x_dim = 640
y_dim = 480

half_x_dim = int(x_dim / 2)
half_y_dim = int(y_dim / 2)

lower_bound = half_x_dim - int(x_dim / 4)
upper_bound = half_x_dim + int(x_dim / 4)
lower_bound_hard = half_x_dim - int(x_dim / 10)
upper_bound_hard = half_x_dim + int(x_dim / 10)
max_frame_difference = 255 * x_dim * y_dim

canny_min = 100
canny_max = 120

prev_c_x, prev_c_y = 0, 180
c_x, c_y = 0, 180

vector_min_x = int(x_dim / 10)
vector_min_y = int(y_dim / 10)

frames_before_refresh = 3

magnitude_threshold = 0.004
max_magnitude_threshold = 0.025

prev_img = []


def matrix_sum(mat):
    arrsum = 0
    y_size = len(mat)
    for i in range(y_size):
        arrsum += sum(mat[i])
    return arrsum / max_frame_difference


camera = PiCamera()
camera.resolution = (x_dim, y_dim)
camera.framerate = 10
rawcap = PiRGBArray(camera, size=(x_dim, y_dim))
time.sleep(0.5)

for frame in camera.capture_continuous(rawcap, format="bgr", use_video_port=True):
    pwm.start(dc)
    frame_count += 1
    if frame_count <= 1:
        prev_img = Frame(frame.array)

    img = Frame(frame.array)

    diff = cv2.subtract(img.blur(2), prev_img.blur(2))
    canny_diff = cv2.Canny(diff, canny_min, canny_max)
    t_res, thresh = cv2.threshold(canny_diff, 127, 255, 0)

    thresh_mag = matrix_sum(thresh)

    moments = cv2.moments(thresh)

    if magnitude_threshold < thresh_mag < max_magnitude_threshold:
        if moments["m00"] != 0:
            c_x = int(moments["m10"] / moments["m00"])
            c_y = int(moments["m01"] / moments["m00"])

    centroid_vec_x = c_x - prev_c_x
    centroid_vec_y = c_y - prev_c_y

    if abs(centroid_vec_x) < vector_min_x:
        centroid_vec_x = 0
    if abs(centroid_vec_y) < vector_min_y:
        centroid_vec_y = 0
    print(" > Mvmnt Mag:", thresh_mag)
    print(lower_bound, lower_bound_hard, c_x, upper_bound_hard, upper_bound)
    if reset_count > 1:
        if lower_bound < c_x < upper_bound:
            print(" > set dc to 60")
            dc = 60
            print("  >> close to center")
            if lower_bound_hard < c_x < upper_bound_hard:
                dc = 0
                dbconn.execute_commit("")
                print("  >> at center")
                print(" >>> picking up item...")
                time.sleep(1)
                print(" >>> robot moving, please wait...")
                time.sleep(1)
                print(" >>> robot moving, please wait...")
                time.sleep(1)
                print(" >>> item picked up!")

        else:
            print(" > set dc to 80")
            dc = 90
    if frame_count % frames_before_refresh == 0:
        print("--reset")
        reset_count += 1
        prev_img = Frame(frame.array)
        c_x, c_y = 0, 0
    cv2.circle(thresh, (c_x, half_y_dim), 5, (255, 255, 255), -1)
    cv2.imshow("Difference Frame", thresh)
    prev_c_x, prev_c_y = c_x, c_y

    rawcap.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
exit()
