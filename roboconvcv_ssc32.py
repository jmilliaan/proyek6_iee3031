import serial.serialutil

import ssc32
import time


class SSC32RoboticArm:
    def __init__(self, port, baud):
        self.default_dur = 800
        self.extended_dur = 1600
        self.serial_port = port
        self.baud_rate = baud
        self.connected = False
        try:
            self.ssc = ssc32.SSC32(self.serial_port, self.baud_rate)
            self.connected = True
        except serial.serialutil.SerialException:
            print(f"Port {self.serial_port} not found.")
            self.connected = False
            pass

    def move_ssc(self, servo, pos, dur):
        if self.connected:
            self.ssc[servo].position = pos
            self.ssc.commit(time=dur)

    def reset_position(self):
        if self.connected:
            print("||| SSC32 RESET POSITION |||")
            self.move_ssc(0, 1500, self.extended_dur)
            self.move_ssc(1, 1500, self.extended_dur)
            self.move_ssc(2, 1500, self.extended_dur)
            self.move_ssc(3, 1500, self.extended_dur)
            self.move_ssc(4, 1000, self.extended_dur)

    def ready_position(self):
        if self.connected:
            print("||| SSC32 READY POSITION |||")
            self.move_ssc(0, 2400, self.extended_dur)
            self.move_ssc(1, 1600, self.extended_dur)
            self.move_ssc(2, 1200, self.extended_dur)
            self.move_ssc(3, 1350, self.extended_dur)
            self.move_ssc(4, 2400, self.extended_dur)

    def grab_position(self):
        if self.connected:
            print("||| SSC32 GRAB POSITION |||")
            self.move_ssc(0, 2400, self.default_dur)
            self.move_ssc(1, 1400, self.default_dur)
            self.move_ssc(2, 1200, self.default_dur)
            self.move_ssc(3, 1150, self.default_dur)
            time.sleep(self.default_dur / 1000)
            self.move_ssc(4, 1000, self.default_dur)
            time.sleep(2 * self.default_dur / 1000)
            self.move_ssc(4, 2400, self.default_dur)

    def drop_position(self):
        if self.connected:
            print("||| SSC32 DROP POSITION |||")
            self.move_ssc(0, 1500, self.default_dur)
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
