
import os
import pickle

names = []
encodings = []

for dir in os.listdir("images"):
    for p, d, fs in os.walk(f"images/{dir}"):
        for f in fs:
            if f.split('.')[1] == 'pickle':
                with open(f"{p}/{f}", 'rb') as file:
                    image_details = pickle.load(file)
                    if len(image_details["encodings"]) == 1:
                        encodings.append(image_details["encodings"][0])
                        names.append(p.split('/')[1])

with open("images/catalogue.pickle", "wb") as output_file:
    output_file.write(pickle.dumps({"names":names, "encodings":encodings}))


    
