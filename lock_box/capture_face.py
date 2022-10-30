import sys
import time
import pickle

from uuid import uuid4

from face_recognition import face_encodings, face_landmarks

from common import take_image, save_image, detect_faces, draw_boxes, draw_lines, create_folder

folder = sys.argv[1]
number_of_images = int(sys.argv[2])

def take_images_detect_encode_save(folder='unknown', number_of_images=10, pause=0.2):
    for n in range(number_of_images):
        unique = uuid4().hex
        #Take image
        image = take_image()
        faces = detect_faces(image)
        if len(faces) > 0:
            create_folder(folder)
            encodings = face_encodings(image, faces)
            landmarks = face_landmarks(image, faces)
            image = draw_boxes(image, faces)
            image = draw_lines(image, landmarks)
            save_image(image, unique, folder)

            data = {"faces":faces, 
                "landmarks":landmarks, 
                "encodings":encodings
                }

            with open(f"images/{folder}/{unique}_encodings.pickle", "wb") as output_file:
                output_file.write(pickle.dumps(data))

        if n < number_of_images - 1:
            time.sleep(pause)


take_images_detect_encode_save(folder, number_of_images)
