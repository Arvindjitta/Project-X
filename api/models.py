from django.db import models
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
# from api.views import get_last_cover

def upload_path(instance, filname):
    return '/'.join(['covers', str(instance.title), filname])

class Book(models.Model):
    title = models.CharField(max_length=32, blank=False)
    cover = models.ImageField(blank=True, null=True, upload_to=upload_path)


    def __str__(self):     #this code makes you see title in admin page
        return self.title


