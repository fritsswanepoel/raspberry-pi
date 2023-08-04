import RPi.GPIO as GPIO
import time
from datetime import datetime

import pickle
from face_recognition import compare_faces, face_encodings

import lcd_control
from common import take_image, detect_faces

GPIO.setmode(GPIO.BCM)

##Allowed people
ALLOWED_PEOPLE = ['danielle','frits']

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
        person_results = {}

        counter = 0
        for encoding in catalogue["encodings"]:
            person = catalogue["names"][counter]
            if person not in person_results:
                person_results[person] = {"correct":0.0, "total":0.0}

            if compare_faces(encoding, new_encoding, tolerance=0.6)[0]:
                person_results[person]["correct"] += 1.0
            
            person_results[person]["total"] += 1.0

            counter += 1

        most_likely = 'unknown'
        top_score = 0.0
        for person in person_results:
            if person_results[person]['correct'] / person_results[person]['total'] > top_score:
                top_score = person_results[person]['correct'] / person_results[person]['total']
                most_likely = person
            
            if top_score == 1.0:
                break

        for per in person_results:
            print(f"{per.title()} matched {person_results[per]['correct']} / {person_results[per]['total']}")

        print(f"{person.title()} matched most with {int(top_score*100)}%")

        return (True, person)

    else:
        return (False, faces)

#Clear LCD
lcd_control.lcd_byte(0x01, lcd_control.LCD_CMD)

#Load known faces
with open('images/catalogue.pickle','rb') as file:
    catalogue = pickle.load(file)

lcd_control.lcd_string("Ready")
for count_down in range(3):
    for led in [LED_GREEN, LED_RED]:
        for state in [GPIO.HIGH, GPIO.LOW]:
            GPIO.output(led, state)
            time.sleep(0.1)

#Clear LCD
lcd_control.lcd_byte(0x01, lcd_control.LCD_CMD)

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

            lcd_control.lcd_string("Confirming")
            lcd_control.lcd_string("identity...", lcd_control.LCD_LINE_2)
            check, person = check_face()

            if check and person in ALLOWED_PEOPLE:
                lcd_control.lcd_string("Access granted")
                lcd_control.lcd_string(person.title(), lcd_control.LCD_LINE_2)
                time.sleep(0.5)
                # Open door
                servo.ChangeDutyCycle(4)
                time.sleep(0.1)
                servo.ChangeDutyCycle(0)
                lock_position = 0
                lcd_control.lcd_string("Door open!")
                lcd_control.lcd_string("", lcd_control.LCD_LINE_2)
            elif check and person not in ALLOWED_PEOPLE:
                lcd_control.lcd_string("Access denied!")
                lcd_control.lcd_string(person.title(), lcd_control.LCD_LINE_2)
                for count_down in range(10):
                    for state in [GPIO.HIGH, GPIO.LOW]:
                        GPIO.output(LED_RED, state)
                        time.sleep(0.1)
            elif not check:
                lcd_control.lcd_string("Technical issue")
                lcd_control.lcd_string(":(", lcd_control.LCD_LINE_2)
                if len(person) > 1:
                    lcd_control.lcd_string(f"{person} faces", lcd_control.LCD_LINE_2)
                for count_down in range(10):
                    for state in [GPIO.HIGH, GPIO.LOW]:
                        GPIO.output(LED_GREEN, state)
                        time.sleep(0.1)

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
            lcd_control.lcd_string("", lcd_control.LCD_LINE_2)

        #To display
        time.sleep(3)

        #Reset LED and LCD
        reset_all()
    else:
        print("Too soon to press the button again!")
