import cv2

def face_detection(img):
    #Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #Convert to greyscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Detect faces
    faces = face_cascade.detectMultiScale(
        gray, #Image
        scaleFactor = 1.1, #Scale factor
        minNeighbors = 4, # minNeighbors
        minSize = (30, 30) #minSize
        )

    return faces