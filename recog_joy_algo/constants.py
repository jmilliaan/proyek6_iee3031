import json

json_file = open("constants.json")
constants = json.load(json_file)

mqtt = constants["MQTT"]
mqtt_username = mqtt["username"]
mqtt_password = mqtt["password"]
mqtt_topic = mqtt["topic"]
mqtt_ip = mqtt["ip"]

mysql = constants["MySQL"]
mysql_username = mysql["username"]
mysql_password = mysql["password"]
mysql_ip = mysql["ip"]

ssc32 = constants["SSC32"]
ssc32_mode = ssc32["mode"]

cv = constants["OpenCV"]
cv_x_dim = cv["x_dim"]
cv_y_dim = cv["y_dim"]
cv_max_pixel = cv["max_pixel"]
cv_canny_min = cv["canny_min"]
cv_canny_max = cv["canny_max"]
cv_prev_c_x = cv["prev_c_x"]
cv_prev_c_y = cv["prev_c_y"]
cv_frames_before_refresh = cv["frames_before_refresh"]
cv_magnitude_lower_boundary = cv["magnitude_lower_boundary"]
cv_magnitude_upper_boundary = cv["magnitude_upper_boundary"]

conveyor = constants["ConveyorBelt"]
conveyor_pwm_pin = conveyor["PWM_pin"]
conveyor_high_dc = conveyor["high_dc"]
conveyor_low_dc = conveyor["low_dc"]
conveyor_stop_dc = conveyor["stop_dc"]

mqtt_username = constants["MQTT"]["username"]
password = "191900103"
topic = "channel"

broker_ip = "10.252.243.158"

db_host_ip = "10.252.242.117"
mode = 1

ch1_prev = 0
ch2_prev = 0
ch3_prev = 0
ch4_prev = 0

controlpin = 14

dc = 90

cycle_count = 0
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
