from rest_framework import viewsets
#added
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from api.models import Book
import random
import string
import glob
import base64
#added
from django.http import HttpResponse
from .serializers import BookSerializer
# from .models import Book
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
import os
from django.db.models import ForeignKey

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



    # def post(self, request, *args, **kwargs):
def get_last_cover(request): 
    if request.method == 'GET':
        def detect_faces(img_name):
            known_face_encodings = np.load(os.getcwd()+'/api/face_encodings.npy', allow_pickle=True)
            known_face_names = np.load(os.getcwd()+'/api/names.npy', allow_pickle=True)

            # Load an image with an unknown face
            unknown_image = face_recognition.load_image_file(img_name)

            # Find all the faces and face encodings in the unknown image
            face_locations = face_recognition.face_locations(unknown_image)
            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            pil_image = Image.fromarray(unknown_image)
            # Create a Pillow ImageDraw Draw instance to draw with
            draw = ImageDraw.Draw(pil_image)

            students_present = []
            # Loop through each face found in the unknown image
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = str(known_face_names[best_match_index])
                    students_present.append(name)

                # Draw a box around the face using the Pillow module
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

                # Draw a label with a name below the face
                text_width, text_height = draw.textsize(name)
                draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
                draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
                # >>>>>added
                # pil_image_io = StringIO()
                # pil_image.save(pil_image_io, format='JPEG')
                # pil_image_file = InMemoryUploadedFile(pil_image_io, None, 'foo.jpg', 'image/jpeg',
                #                   pil_image_io.len, None)
                
                # pil_image.save('C:/Users/yashw/OneDrive/Desktop/projects/Project-X/api/output1.jpg')
                # pil_image.save(os.path.abspath("media/'kotlak/") + '.JPG' , 'JPEG')
                # instance.pil_image.path = 'covers/new-path.avi'
                # Book.objects.all().last().update(cover = b)
                def get_random_string(length):
                    letters = string.ascii_lowercase
                    result_str = ''.join(random.choice(letters) for i in range(length))
                    return result_str
                new_string = get_random_string(8)
                file_path = os.path.abspath(f"modia/covers/output/{new_string}/") + '.jpg'
                ret_path = 'modia/covers/output/'+new_string+'.jpg'
                pil_image.save(file_path , 'jpeg')
    
                # c = Book.objects.all().last()
                # list_of_files = glob.glob('modia/covers/output/*') # * means all if need specific format then *.csv
                # latest_file = max(list_of_files, key=os.path.getctime)
                # print(latest_file)
                # c.cover = os.path.abspath("media/kotlak.JPG")
                # c.cover = max(list_of_files, key=os.path.getctime)
                # c.save()
            return ret_path
        #added
        image_path = Book.objects.all().last().cover.path
        # image_path =  Book.objects.get(title='Bill gates').cover.path
        # image_path = os.path.abspath("api/kotla.jpg")ss
        ret_path = detect_faces(image_path)
        last_cover = Book.objects.all().last()
        # serializer = BookSerializer(last_cover, context={"request": request})
        # serializer = BookSerializer(last_cover)
        resp_data = {
            'resp':ret_path
        }
        return JsonResponse(resp_data,safe=True)
        #added

def get_last_cover_before_search(request):    
    if request.method == 'GET':
        last_cover= Book.objects.all().last()
        serializer = BookSerializer(last_cover)
        return JsonResponse(serializer.data, safe=False)

