from picamera.array import PiRGBArray as pi_rgb
from picamera import PiCamera as picam
from scipy.ndimage.filters import gaussian_filter
from datetime import datetime
import cv2
import time
import paho.mqtt.client as mqtt
import mysql.connector
import RPi.GPIO as GPIO
import json
import numpy as np
import serial.serialutil
import serial
import ssc32

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

json_file = open("json")
constants = json.load(json_file)

# MQTT CONSTANTS
mqtt_const = constants["MQTT"]
mqtt_username = mqtt_const["username"]
mqtt_password = mqtt_const["password"]
mqtt_topic = mqtt_const["topic"]
mqtt_ip = mqtt_const["ip"]

# MYSQL CONSTANTS
mysql_const = constants["MySQL"]
mysql_username = mysql_const["username"]
mysql_password = mysql_const["password"]
mysql_ip = mysql_const["ip"]

# SSC32 CONSTANTS
ssc32_const = constants["SSC32"]
ssc32_mode = ssc32_const["mode"]
ssc32_serial_port = ssc32_const["serial_port"]
ssc32_baud_rate = ssc32_const["baud_rate"]

# OPENCV CONSTANTS
cv = constants["OpenCV"]

cv_framerate = cv["frame_rate"]

cv_x_dim = cv["x_dim"]
cv_y_dim = cv["y_dim"]
cv_resolution = (cv_x_dim, cv_y_dim)

cv_half_x_dim = cv_x_dim // 2
cv_half_y_dim = cv_y_dim // 2

cv_lower_bound = cv_half_x_dim - cv_half_x_dim // 2
cv_upper_bound = cv_half_x_dim + cv_half_x_dim // 2

cv_hard_lower_bound = cv_half_x_dim - cv_half_x_dim // 5
cv_hard_upper_bound = cv_half_x_dim + cv_half_x_dim // 5

cv_max_pixel = cv["max_pixel"]
cv_max_frame_difference = cv_max_pixel * cv_x_dim * cv_y_dim

cv_vector_min_x = cv_x_dim // 10
cv_vector_min_y = cv_y_dim // 10

cv_canny_min = cv["canny_min"]
cv_canny_max = cv["canny_max"]
cv_prev_c_x = cv["prev_c_x"]
cv_prev_c_y = cv["prev_c_y"]
cv_frames_before_refresh = cv["frames_before_refresh"]
cv_magnitude_lower_boundary = cv["magnitude_lower_boundary"] * cv_max_frame_difference
cv_magnitude_upper_boundary = cv["magnitude_upper_boundary"] * cv_max_frame_difference

# CONVEYOR BELT CONSTANTS
conveyor = constants["ConveyorBelt"]
conveyor_pwm_pin = conveyor["PWM_pin"]
conveyor_high_dc = conveyor["high_dc"]
conveyor_low_dc = conveyor["low_dc"]
conveyor_stop_dc = conveyor["stop_dc"]
conveyor_frequency = conveyor["PWM_freq"]

json_file.close()


class ConveyorBelt:
    def __init__(self):
        GPIO.setup(conveyor_pwm_pin,
                   GPIO.OUT)
        self.pwm = GPIO.PWM(conveyor_pwm_pin,
                            conveyor_frequency)

    def start(self):
        self.pwm.start(conveyor_high_dc)
        time.sleep(0.1)

    def change_dc(self, dc):
        print(f"Duty Cycle: {dc}%")
        self.pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)


class DBConnection:
    def __init__(self):
        self.host_ip = mysql_ip
        self.user = mysql_username
        self.password = mysql_password
        self.connected = False
        self.table_name = "event_logging"

        try:
            self.mydb = mysql.connector.connect(host=self.host_ip,
                                                user=self.user,
                                                password=self.password)
            self.c = self.mydb.cursor()
            print("Connected to MySQL Server at:", self.host_ip, "\nAs user:", self.user)
            self.execute_commit("USE Proyek6_IEE3031;")
            self.connected = True

        except:
            print("Failed To Connect to DB.")
            self.connected = False
            pass

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def get_date():
        return datetime.now().strftime("%d-%m-%Y")

    def commit(self):
        if self.connected:
            self.mydb.commit()

    def execute(self, query):
        if self.connected:
            self.c.execute(query)

    def execute_commit(self, query):
        if self.connected:
            self.execute("USE Proyek6_IEE3031;")
            self.c.execute(query)
            self.commit()

    def log_start_conv(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(), "Conveyor starting.")

    def log_slow_conv(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(),
                     "Item near grabbing position. "
                     "Conveyor Belt slowing down.")

    def log_stop_conv(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(), "Item at grabbing position. Conveyor stopping.")

    def log_ssc_take_item(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(), "Item at grabbing position. SSC32 Robot Arm taking object.")

    def log(self, current_time, current_date, event):
        if self.connected:
            self.execute_commit(f"INSERT INTO {self.table_name}"
                                f"(time, date, event) "
                                f"VALUES('{current_time}', '{current_date}', '{event}');")

    def print_c(self):
        if self.connected:
            for i in self.c.fetchall():
                print(i)
        else:
            pass

    def reconnect(self):
        try:
            self.mydb = mysql.connector.connect(host=mysql_ip,
                                                user=mysql_username,
                                                password=mysql_password)
            self.c = self.mydb.cursor()
            self.connected = True
        except:
            print("Failed to Reconnect to DB.")
            self.connected = False
            pass


class Frame:
    def __init__(self, fr):
        self.raw_frame = fr
        self.bw = cv2.cvtColor(self.raw_frame, cv2.COLOR_BGR2GRAY)
        self.canny_min = cv_canny_min
        self.canny_max = cv_canny_max
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

    def canny(self, im, minval, maxval):
        cannydetector = cv2.Canny(im, minval, maxval)
        self.cannydetector = cannydetector
        return cannydetector

    def canny_difference(self, prev_frame):
        diff = cv2.subtract(self.blurred, prev_frame.blurred)
        return self.canny(diff, self.canny_min, self.canny_max)
        # return diff

    @staticmethod
    def fast_sum_image(src):
        return np.sum(src)

    def centroid(self, im):
        self.frame_moments = cv2.moments(im)
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
        self.cam.resolution = cv_resolution
        self.cam.framerate = cv_framerate
        self.raw_cap = pi_rgb(picam, size=self.cam.resolution)
        time.sleep(0.1)


class MQTT:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        try:
            print(f"Connected {str(rc)}")
            self.client.subscribe(mqtt_topic)
            self.connected = True
        except:
            self.connected = False
            pass

    @staticmethod
    def on_message(client, userdata, msg):
        incoming = msg.payload.decode("utf-8")
        data_list = incoming.split()
        return data_list

    def begin_mqtt(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(mqtt_ip, 1883)
        self.client.loop()
        self.client.disconnect()


class SSC32RoboticArm:
    def __init__(self, port, baud):
        self.default_dur = 800
        self.extended_dur = 1600
        self.serial_port = port
        self.baud_rate = baud
        self.connected = False
        # try:
        #     self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        #     print(f"Connected to {self.serial_port, self.ser}")
        #     self.connected = True
        # except serial.serialutil.SerialException:
        #     self.connected = False
        #     print(f"Serial port {self.serial_port} not found")
        #     pass
        try:
            self.ssc = ssc32.SSC32(self.serial_port, self.baud_rate)
            self.connected = True
        except serial.serialutil.SerialException:
            print(f"Port {self.serial_port} not found.")
            self.connected = False
            pass

    def move_ssc(self, servo, pos, dur):
        if self.connected:
            # self.ser.write(bytes(f"#{servo} P{pos} T{dur} <cr>", "utf-8"))
            self.ssc.commit(time=dur)
            self.ssc[servo].position = pos

    def reset_position(self):
        if self.connected:
            print("||| SSC32 RESET POSITION |||")
            self.move_ssc(0, 2400, self.extended_dur)
            self.move_ssc(1, 1600, self.extended_dur)
            self.move_ssc(2, 2000, self.extended_dur)
            self.move_ssc(3, 1000, self.extended_dur)
            self.move_ssc(4, 1000, self.extended_dur)

    def ready_position(self):
        if self.connected:
            print("||| SSC32 READY POSITION |||")
            self.move_ssc(0, 1400, self.extended_dur)
            self.move_ssc(1, 1400, self.extended_dur)
            self.move_ssc(2, 1800, self.extended_dur)
            self.move_ssc(3, 1000, self.extended_dur)
            self.move_ssc(4, 1000, self.extended_dur)

    def grab_position(self):
        if self.connected:
            print("||| SSC32 GRAB POSITION |||")
            self.move_ssc(0, 1400, self.default_dur)
            self.move_ssc(1, 1400, self.default_dur)
            self.move_ssc(2, 1800, self.default_dur)
            self.move_ssc(3, 1000, self.default_dur)
            time.sleep(self.default_dur / 1000)
            self.move_ssc(4, 1000, self.default_dur)
            time.sleep(2 * self.default_dur / 1000)
            self.move_ssc(4, 2400, self.default_dur)

    def drop_position(self):
        if self.connected:
            print("||| SSC32 DROP POSITION |||")
            self.move_ssc(0, 2400, self.default_dur)
            self.move_ssc(1, 1700, self.default_dur)
            self.move_ssc(2, 1300, self.default_dur)
            self.move_ssc(3, 1350, self.default_dur)
            time.sleep(self.default_dur / 1000)
            self.move_ssc(4, 2400, self.default_dur)
            time.sleep(self.default_dur / 1000)
            self.move_ssc(4, 1000, self.default_dur)

    def reset_ready(self, dur):
        if self.connected:
            self.reset_position()
            time.sleep(dur)
            self.ready_position()
            time.sleep(dur)

    def grab_drop_ready(self, dur):
        if self.connected:
            self.grab_position()
            time.sleep(dur)
            self.drop_position()
            time.sleep(dur)
            self.ready_position()
            time.sleep(dur)


if __name__ == '__main__':
    db = DBConnection()
    robo_arm = SSC32RoboticArm(ssc32_serial_port,
                               ssc32_baud_rate)
    conveyor = ConveyorBelt()
    camera = PiCam()
    conveyor.start()

    frame_count = 0
    reset_count = 0

    prev_img = []

    prev_c_x, prev_c_y = 0, 0
    c_x, c_y = 0, 0

    robo_arm.reset_ready(2)

    for frame in camera.cam.capture_continuous(camera.raw_cap,
                                               format="bgr",
                                               use_video_port=True):
        img = Frame(frame.array)

        if frame_count <= 1:
            prev_img = Frame(frame.array)

        if frame_count % cv_frames_before_refresh == 0:
            reset_count += 1
            prev_img = Frame(frame.array)

        canny_diff = img.canny_difference(prev_img)
        magnitude = img.fast_sum_image(canny_diff)
        c_x, c_y = img.centroid(canny_diff)

        # cv2.circle(canny_diff, (c_x, c_y), 5, (255, 255, 255), -1)

        # cv2.imshow("Difference Frame", canny_diff)
        # cv2.imshow("Canny Frame", img.canny_edges)

        centroid_pos_condition = cv_hard_lower_bound < c_x < cv_hard_upper_bound
        magnitude_size_condition = cv_magnitude_lower_boundary < magnitude <  \
            cv_magnitude_upper_boundary

        print(f"FRAME: {frame_count}")
        print(f" > Movement Magnitude : {magnitude_size_condition} : ", end=" ")
        print(
            f"{cv_magnitude_lower_boundary} < {magnitude} < {cv_magnitude_upper_boundary}")
        print(f" > Centroid: {centroid_pos_condition} : ", end=" ")
        print(f"{cv_lower_bound} < "
              f"{cv_hard_lower_bound} < "
              f"{c_x} < "
              f"{cv_hard_upper_bound} < "
              f"{cv_upper_bound}")

        if cv_lower_bound < c_x < cv_upper_bound:
            print(" >> close to center")
            conveyor.change_dc(conveyor_low_dc)

            if centroid_pos_condition and magnitude_size_condition:
                print(" >>> at center", end=" ")
                print(cv_hard_lower_bound,
                      c_x,
                      cv_hard_upper_bound)
                conveyor.change_dc(conveyor_stop_dc)

                time.sleep(0.5)
                robo_arm.grab_drop_ready(1)

                magnitude = 0
                c_x, c_y = 0, 0
                camera.raw_cap.truncate(0)
                time.sleep(0.5)
                continue

        else:

            conveyor.change_dc(conveyor_high_dc)

        prev_c_x, prev_c_y = c_x, c_y

        camera.raw_cap.truncate(0)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    exit()
