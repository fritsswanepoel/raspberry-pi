# About
This program is to run facial recognition to control access to a lock box with a servo. 

Facial recognition via a USB webcam.

# References
References used to create this code are:
- https://raspberrypi-guide.github.io/electronics/using-usb-webcams
- https://raspberrypi-guide.github.io/programming/install-opencv.html
- https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81?gi=39a8b914915d
- https://github.com/PacktPublishing/OpenCV-3-x-with-Python-By-Example/issues/2 
- https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition

# Checking webcam
### In terminal
- Plug in webcam
- In termial run lsusb

Webcam should be listed in the set of devices. For the webcam used in this project the entry is:

Bus 001 Device 008: ID 046d:0825 Logitech, Inc. Webcam C270

It's possible to install and control the webcam via the terminal, but not required for this project so skipped.

- Install OpenCV
--In terminal

sudo apt-get update

sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y

pip install -U numpy
pip install opencv-python==4.5.3.56

pip install face-recognition

Terminal showed:

Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting opencv-python
  Downloading https://www.piwheels.org/simple/opencv-python/opencv_python-4.6.0.66-cp39-cp39-linux_armv7l.whl (11.3 MB)
     |████████████████████████████████| 11.3 MB 27 kB/s 
Requirement already satisfied: numpy>=1.19.3 in /usr/lib/python3/dist-packages (from opencv-python) (1.19.5)
Installing collected packages: opencv-python
Successfully installed opencv-python-4.6.0.66

--Test correctly installed, in terminal

python3

In python
import cv2
cv2.__version__

### To stream input until keypress

while True:
    ret, image = cam.read()
    cv2.imshow('Imagetest',image)
    k = cv2.waitKey(1)
    if k != -1:
        break


# Face detection
Tested with: 

'''
import face_recognition

def face_detection(img):
    boxes = face_recognition.face_locations(img, model='hog')
    return boxes
'''

And compared against:

face_cascade.detectMultiScale(
        gray, #Image
        scaleFactor = 1.1, #Scale factor
        minNeighbors = 4, # minNeighbors
        minSize = (30, 30) #minSize
        )

Face cascade is ~5 times faster than face recognition and they identify very similar areas



# Draw box around face
#Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    detected = True
    #Only detect one face
    break
#Display the result
return detected, img