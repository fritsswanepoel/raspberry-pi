import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time

GPIO.setmode(GPIO.BCM)

##Button
def button_callback(channel):
    print("Button was pushed!")

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(23, GPIO.RISING, callback = button_callback)


