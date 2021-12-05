import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pwmpin = 18
dc1 = 100
dc2 = 60
GPIO.setup(pwmpin, GPIO.OUT)
pwm = GPIO.PWM(pwmpin, 100)

while True:
    print("dc: 100%")
    pwm.start(dc1)
    time.sleep(2)
    print("dc: 60%")
    pwm.start(dc2)
    time.sleep(2)
GPIO.cleanup()