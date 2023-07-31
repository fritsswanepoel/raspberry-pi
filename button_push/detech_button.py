import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

##Button
def button_callback(channel):
    print("Button was pushed!")

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(23, GPIO.RISING, callback = button_callback)

time.sleep(3)

GPIO.cleanup()


#Only True when more than 1 second since last press
def button_callback(channel):
    global button_press_time
    last_pressed = datetime.now() - button_press_time 
    if last_pressed.total_seconds() > 1:
        return True
    else:
        return False