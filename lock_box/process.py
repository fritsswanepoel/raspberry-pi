import RPi.GPIO as GPIO
import time
from datetime import datetime

import pickle
from face_recognition import compare_faces, face_encodings

import lcd_control
from facial_recognition.common import take_image, detect_faces

GPIO.setmode(GPIO.BCM)

##Pins
BUTTON = 23

LED_GREEN = 17
LED_RED = 27

SERVO = 18

##Button
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button

GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

GPIO.setup(SERVO, GPIO.OUT)

##Variables
lock_position = 1
button_press_time = datetime.now()


##Servo
servo = GPIO.PWM(SERVO, 50)
servo.start(0)

"""
Flow:
1) Button pushed
2) Orange LED flashes
3) LCD count-down
4) Take photo
5) Most likely candidate
6) Is in allowed list?
7) Is in blocked list?
8) Red light and access denied or orange light and open
9) Button pushed - assume door closed and latch
"""

def reset_all():
    #LED
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_RED, GPIO.LOW)
    #LCD
    lcd_control.lcd_byte(0x01, lcd_control.LCD_CMD)

def check_face():
    #Capture new face
    image = take_image()
    faces = detect_faces(image)
    if len(faces) == 1:
        new_encoding = face_encodings(image, faces)

        #Compare new face to encodings
        results = []

        for encoding in catalogue["encodings"]:
            results.append(compare_faces(encoding, new_encoding, tolerance=0.6)[0])
        
        #print(results)
        person = 'unknown'

        counter = 0
        for result in results:
            print(counter, catalogue["names"][counter], result)
            if result:
                person = catalogue["names"][counter]
                break
            counter += 1

        print(person)

    else:
        print(f"{len(faces)} faces found")
        print(faces)

#Clear LCD
lcd_control.lcd_byte(0x01, lcd_control.LCD_CMD)

#Load known faces
with open('images/catalogue.pickle','rb') as file:
    catalogue = pickle.load(file)


while True:
    ##Button press
    GPIO.wait_for_edge(BUTTON, GPIO.RISING)
    ##Check for time since last press
    last_pressed = datetime.now() - button_press_time 
    if last_pressed.total_seconds() > 1:
        print("Button pushed")
        button_press_time = datetime.now()
        #Check if door is locked
        if lock_position == 1:
            lcd_control.lcd_string("Be ready in")
            for count_down in range(3):
                lcd_control.lcd_string(str(3-count_down), lcd_control.LCD_LINE_2)
                for state in [GPIO.HIGH, GPIO.LOW]:
                    GPIO.output(LED_GREEN, state)
                    time.sleep(0.5)
            check_face()
            # Open door
            servo.ChangeDutyCycle(4)
            time.sleep(0.1)
            servo.ChangeDutyCycle(0)
            lock_position = 0
            lcd_control.lcd_string("Door open!")
        else:
            lcd_control.lcd_string("Locking in")
            for count_down in range(3):
                lcd_control.lcd_string(str(3-count_down), lcd_control.LCD_LINE_2)
                for state in [GPIO.HIGH, GPIO.LOW]:
                    GPIO.output(LED_GREEN, state)
                    time.sleep(0.5)
            # Close door
            servo.ChangeDutyCycle(2)
            time.sleep(0.1)
            servo.ChangeDutyCycle(0)
            lock_position = 1
            lcd_control.lcd_string("Door locked")

        #To display
        time.sleep(3)

        #Reset LED and LCD
        reset_all()
    else:
        print("Too soon to press the button again!")
