from typing import Pattern
from django.db import models
from web_project.settings import BASE_DIR
from pathlib import Path
import uuid  
import datetime
from django.core.files import File
# Create your models here.

user_id = str(uuid.uuid1())
# Create your models here.
def file_name(instance, filename):
    #create the path
    parent = Path('data_set')
    path = Path.joinpath(parent,user_id)
    path = Path.joinpath(path,filename)
    #return the temporary path 
    return path

class Data_set(models.Model):
    #Add a File field to upload the files
    #and set the upload location to the return of the file_name function where the arguments are supplied by django itself
    file = models.FileField(max_length=255, upload_to= file_name)
    #create for each user a unique id to reqonize wich user is visualizing which data set
    user_id = models.CharField(default= user_id, max_length=255)
    #save the time when the user summited the data so that it can be determined when the data should be errased
    time = models.DateTimeField(default= datetime.datetime.now().isoformat())



