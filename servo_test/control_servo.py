import RPi.GPIO as GPIO
import time
from datetime import datetime


GPIO.setmode(GPIO.BCM)



SERVO = 18


GPIO.setup(SERVO, GPIO.OUT)



##Servo
servo = GPIO.PWM(SERVO, 50)


servo.start(0)
servo.ChangeDutyCycle(4)
time.sleep(0.1)
servo.ChangeDutyCycle(0)
time.sleep(0.1)
servo.ChangeDutyCycle(2)
time.sleep(0.1)
servo.ChangeDutyCycle(0)
servo.stop()

