import time
import roboconvcv_constants as c
from roboconvcv_ssc32 import SSC32RoboticArm

ssc = SSC32RoboticArm(c.ssc32_serial_port, c.ssc32_baud_rate)

while True:
    ssc.reset_ready(1)
    time.sleep(2)
    ssc.grab_position()
    time.sleep(2)
    ssc.drop_position()
    time.sleep(2)
    print("cycle done")
