import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LED_GREEN = 17
LED_RED = 27

#Set up GPIO
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

#Turn each LED on and off
for led in [LED_GREEN, LED_RED]:
    GPIO.output(led, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(led, GPIO.LOW)

GPIO.cleanup()