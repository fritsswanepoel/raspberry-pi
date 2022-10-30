
import pickle

from face_recognition import compare_faces, face_encodings

from common import take_image, detect_faces

#Current knowledge
with open('images/catalogue.pickle','rb') as file:
    catalogue = pickle.load(file)

#print(catalogue["names"])

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