from roboconvcv_ssc32 import SSC32RoboticArm
import roboconvcv_constants as constants
import time
port = "COM10"
s = SSC32RoboticArm(port, constants.ssc32_baud_rate)


# s.move_ssc(0, 1400, 1000)
# s.move_ssc(1, 1600, 1000)
# s.move_ssc(2, 2000, 1000)
# s.move_ssc(3, 1000, 1000)
# s.move_ssc(4, 1000, 1000)


for i in range(0, 2000, 50):
    print(i)
    s.move_ssc(5, i, 1500)
    time.sleep(0.2)