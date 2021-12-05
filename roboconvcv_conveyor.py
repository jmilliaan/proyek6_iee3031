import RPi.GPIO as GPIO
import roboconvcv_constants as constants
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class ConveyorBelt:
    def __init__(self):
        GPIO.setup(constants.conveyor_pwm_pin,
                   GPIO.OUT)
        self.pwm = GPIO.PWM(constants.conveyor_pwm_pin,
                            constants.conveyor_frequency)

    def start(self):
        self.pwm.start(constants.conveyor_high_dc)
        time.sleep(0.1)

    def change_dc(self, dc):
        print(f"Duty Cycle: {dc}%")
        self.pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)
