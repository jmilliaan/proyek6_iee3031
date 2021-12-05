import ssc32
import time


class SSC32RoboticArm:
    def __init__(self, port, baud):
        self.ssc = ssc32.SSC32(port, baud)
        self.default_dur = 800

    def move_ssc(self, servo, pos, dur):
        self.ssc[servo].position = pos
        self.ssc.commit(time=dur)

    def reset_position(self):
        print("||| SSC32 RESET POSITION |||")
        self.move_ssc(0, 1500, self.default_dur)
        self.move_ssc(1, 1500, self.default_dur)
        self.move_ssc(2, 1500, self.default_dur)
        self.move_ssc(3, 1500, self.default_dur)
        self.move_ssc(4, 1000, self.default_dur)

    def ready_position(self):
        print("||| SSC32 READY POSITION |||")
        self.move_ssc(0, 2400, self.default_dur)
        self.move_ssc(1, 1700, self.default_dur)
        self.move_ssc(2, 1300, self.default_dur)
        self.move_ssc(3, 1350, self.default_dur)
        self.move_ssc(4, 2400, self.default_dur)

    def grab_position(self):
        print("||| SSC32 GRAB POSITION |||")
        self.move_ssc(0, 2400, self.default_dur)
        self.move_ssc(1, 1350, self.default_dur)
        self.move_ssc(2, 1150, self.default_dur)
        self.move_ssc(3, 1100, self.default_dur)
        time.sleep(self.default_dur / 1000)
        self.move_ssc(4, 1000, self.default_dur)
        time.sleep(2 * self.default_dur / 1000)
        self.move_ssc(4, 2400, self.default_dur)

    def drop_position(self):
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
        self.reset_position()
        time.sleep(dur)
        self.ready_position()
        time.sleep(dur)

    def grab_drop_ready(self, dur):
        self.grab_position()
        time.sleep(dur)
        self.drop_position()
        time.sleep(dur)
        self.ready_position()
        time.sleep(dur)
