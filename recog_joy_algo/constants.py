import json

json_file = open("constants.json")
constants = json.load(json_file)

# MQTT CONSTANTS
mqtt = constants["MQTT"]
mqtt_username = mqtt["username"]
mqtt_password = mqtt["password"]
mqtt_topic = mqtt["topic"]
mqtt_ip = mqtt["ip"]

# MYSQL CONSTANTS
mysql = constants["MySQL"]
mysql_username = mysql["username"]
mysql_password = mysql["password"]
mysql_ip = mysql["ip"]

# SSC32 CONSTANTS
ssc32 = constants["SSC32"]
ssc32_mode = ssc32["mode"]

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
cv_magnitude_lower_boundary = cv["magnitude_lower_boundary"]
cv_magnitude_upper_boundary = cv["magnitude_upper_boundary"]

# CONVEYOR BELT CONSTANTS
conveyor = constants["ConveyorBelt"]
conveyor_pwm_pin = conveyor["PWM_pin"]
conveyor_high_dc = conveyor["high_dc"]
conveyor_low_dc = conveyor["low_dc"]
conveyor_stop_dc = conveyor["stop_dc"]
