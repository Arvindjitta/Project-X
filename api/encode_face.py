import face_recognition
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd

students = pd.read_excel("students_locations.xlsx")
roll_numbers = students[["roll_number","face_path"]]
roll_numbers_np = roll_numbers.to_numpy()
face_encoding = []
names = []
for i in range(0,len(roll_numbers_np)):
    temp = roll_numbers_np[i,1]
    image = face_recognition.load_image_file(temp)
    encodings = face_recognition.face_encodings(image)[0]
    names.append(roll_numbers_np[i,0])
    face_encoding.append(encodings)

np.save( "face_encodings",face_encoding)
np.save( "names",names)