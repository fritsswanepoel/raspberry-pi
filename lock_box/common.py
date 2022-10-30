import os
from uuid import uuid4

import cv2

from shared.box_converter import *


def take_image():
    #Set up connection
    cam = cv2.VideoCapture(0)
    #Capture image
    ret, image = cam.read()
    #Release connection
    cam.release()

    return image


def save_image(image,unique=uuid4().hex,folder='unknown',suffix=''):
    cv2.imwrite(f'images/{folder}/{unique}{suffix}.jpg', image)


def detect_faces(image):
    #Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #Convert to greyscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Detect faces
    faces = face_cascade.detectMultiScale(
        image, #Image
        scaleFactor = 1.1, #Scale factor
        minNeighbors = 4, # minNeighbors
        minSize = (30, 30) #minSize
        )

    return [xywh_to_tlbr(face) for face in faces]


def draw_boxes(image, faces):
    for (t, l, b, r) in faces:
        cv2.rectangle(image, (r, t), (l, b), (255, 0, 0), 3)
    return image


def draw_lines(image, landmarks):
    for landmark in landmarks:
        for feature, position in landmark.items():
            for i in range(len(position)-1):
                cv2.line(image, position[i], position[i+1], (50, 50, 50), 2)
            if feature in ('right_eye','left_eye'):
                cv2.line(image,position[0],position[-1], (50, 50, 50), 2)
    return image

def create_folder(folder):
    if not os.path.exists(f'images/{folder}'):
        os.makedirs(f'images/{folder}')
