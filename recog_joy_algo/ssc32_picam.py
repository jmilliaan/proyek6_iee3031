from picamera.array import PiRGBArray
from picamera import PiCamera
from capture_class import Frame
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
from mysql_proyek6 import DBConnection
import ssc32
import constants

dbconn = DBConnection()
ssc = ssc32.SSC32(constants.ssc32_serial_port,
                  constants.ssc32_baud_rate)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(constants.conveyor_pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(constants.conveyor_pwm_pin, 100)
prev_img = []


def move_ssc(ssc_obj, servo, position, duration):
    ssc_obj[servo].position = position
    ssc_obj.commit(time=duration)


def reset_position(ssc_obj):
    dur = 200
    move_ssc(ssc_obj, 0, 1500, dur)
    move_ssc(ssc_obj, 1, 1500, dur)
    move_ssc(ssc_obj, 2, 1500, dur)
    move_ssc(ssc_obj, 3, 1500, dur)
    move_ssc(ssc_obj, 4, 1000, dur)


def ready_position(ssc_obj):
    dur = 200
    move_ssc(ssc_obj, 0, 2400, dur)
    move_ssc(ssc_obj, 1, 1700, dur)
    move_ssc(ssc_obj, 2, 1300, dur)
    move_ssc(ssc_obj, 3, 1350, dur)
    move_ssc(ssc_obj, 4, 2400, dur)


def grab_position(ssc_obj):
    dur = 200
    move_ssc(ssc_obj, 0, 2400, dur)
    move_ssc(ssc_obj, 1, 1350, dur)
    move_ssc(ssc_obj, 2, 1150, dur)
    move_ssc(ssc_obj, 3, 1100, dur)
    move_ssc(ssc_obj, 4, 1000, dur)


def drop_position(ssc_obj):
    dur = 200
    move_ssc(ssc_obj, 0, 2400, dur)
    move_ssc(ssc_obj, 1, 1700, dur)
    move_ssc(ssc_obj, 2, 1300, dur)
    move_ssc(ssc_obj, 3, 1350, dur)
    move_ssc(ssc_obj, 4, 1000, dur)


def matrix_sum(mat):
    arrsum = 0
    y_size = len(mat)
    for i in range(y_size):
        arrsum += sum(mat[i])
    return arrsum / constants.cv_max_frame_difference


camera = PiCamera()
camera.resolution = constants.cv_resolution
camera.framerate = constants.cv_framerate
rawcap = PiRGBArray(camera, size=camera.resolution)
time.sleep(0.5)

current_dc = constants.conveyor_high_dc
frame_count = 0
reset_count = 0

prev_c_x, prev_c_y = 0, 0
c_x, c_y = 0, 0
if __name__ == '__main__':
    reset_position(ssc)
    time.sleep(1)
    ready_position(ssc)
    time.sleep(0.5)
    for frame in camera.capture_continuous(rawcap, format="bgr", use_video_port=True):

        pwm.start(current_dc)
        frame_count += 1
        if frame_count <= 1:
            prev_img = Frame(frame.array)

        img = Frame(frame.array)

        diff = cv2.subtract(img.blur(2), prev_img.blur(2))
        canny_diff = cv2.Canny(diff, constants.cv_canny_min, constants.cv_canny_max)
        t_res, thresh = cv2.threshold(canny_diff, 127, 255, 0)

        # thresh_mag = matrix_sum(thresh)
        thresh_mag = np.sum(thresh)
        moments = cv2.moments(thresh)

        if constants.cv_magnitude_lower_boundary < thresh_mag < constants.cv_magnitude_upper_boundary:
            if moments["m00"] != 0:
                c_x = int(moments["m10"] / moments["m00"])
                c_y = int(moments["m01"] / moments["m00"])

        centroid_vec_x = c_x - prev_c_x
        centroid_vec_y = c_y - prev_c_y

        if abs(centroid_vec_x) < constants.cv_vector_min_x:
            centroid_vec_x = 0

        if abs(centroid_vec_y) < constants.cv_vector_min_y:
            centroid_vec_y = 0

        print(" > Mvmnt Mag:", thresh_mag)
        print(constants.cv_lower_bound,
              constants.cv_hard_lower_bound,
              c_x,
              constants.cv_hard_upper_bound,
              constants.cv_upper_bound)

        if reset_count > 1:
            if constants.cv_lower_bound < c_x < constants.cv_upper_bound:
                print(" > set dc to 60")
                current_dc = constants.conveyor_low_dc
                print("  >> close to center")
                if constants.cv_hard_lower_bound < c_x < constants.cv_hard_upper_bound:
                    current_dc = constants.conveyor_stop_dc
                    dbconn.execute_commit("")
                    print("  >> at center")
                    print(" >>> picking up item...")
                    
                    grab_position(ssc)
                    time.sleep(1)
                    
                    print(" >>> robot moving, please wait...")
                    time.sleep(0.5)
                    print(" >>> robot moving, please wait...")
                    time.sleep(0.5)
                    print(" >>> item picked up!")
                    drop_position(ssc)
                    time.sleep(0.5)
                    ready_position(ssc)
                    time.sleep(1)
            else:
                print(" > set dc to 80")
                current_dc = constants.conveyor_high_dc

        if frame_count % constants.cv_frames_before_refresh == 0:
            print("--reset")
            reset_count += 1
            prev_img = Frame(frame.array)
            c_x, c_y = 0, 0

        cv2.circle(thresh, (c_x, constants.cv_half_y_dim), 5, (255, 255, 255), -1)
        cv2.imshow("Difference Frame", thresh)
        prev_c_x, prev_c_y = c_x, c_y

        rawcap.truncate(0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    exit()
