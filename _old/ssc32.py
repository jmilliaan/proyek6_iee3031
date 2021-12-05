import RPi.GPIO as GPIO
import ssc32
import numpy as np
import time

from mysql_proyek6 import DBConnection

dbconn = DBConnection()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

username = "jm03"
password = "191900103"
topic = "channel"

# serialport = "/dev/ttyUSB0"
# ssc = ssc32.SSC32(serialport, 9600)

broker_ip = "10.252.243.158"
# client = mqtt.Client()
# client.username_pw_set(username, password)

mode = 1

ch1_prev = 0
ch2_prev = 0
ch3_prev = 0
ch4_prev = 0


def move_ssc(ssc_obj, servo, position, duration):
    ssc_obj[servo].position = position
    ssc_obj.commit(time=duration)
    # ssc.wait_for_movement_completion()


def on_connect(client, userdata, flags, rc):
    print("Connected", str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    global mode
    global ch1_prev
    global ch2_prev
    global ch3_prev
    global ch4_prev

    incoming = msg.payload.decode('utf-8')
    control_list = incoming.split(":")
    button = int(control_list[0])
    ch1 = abs(int(control_list[1])) * 50 + 500
    ch2 = abs(int(control_list[2])) * 50 + 1500
    ch3 = abs(int(control_list[3])) * 50 + 1350
    ch4 = abs(int(control_list[4])) * 50 + 1500

    print()
    if (ch1 == ch1_prev) or (ch2 == ch2_prev) or (ch3 == ch3_prev) or (ch4 == ch4_prev):
        pass
    else:
        move_ssc(0, ch1, 200)
        move_ssc(1, ch2, 200)
        move_ssc(2, ch3, 200)
        move_ssc(3, ch4, 200)
        ch1_prev = ch1
        ch2_prev = ch2
        ch3_prev = ch3
        ch4_prev = ch4
    print(ch1, ch1_prev)
    print(ch2, ch2_prev)
    print(ch3, ch3_prev)
    print(ch4, ch4_prev)
    # time.sleep(0.1)


if __name__ == "__main__":
    # client.on_connect = on_connect
    # client.on_message = on_message

    # client.connect(broker_ip, 1883)
    # client.loop_forever()
    # client.disconnect
    pass
