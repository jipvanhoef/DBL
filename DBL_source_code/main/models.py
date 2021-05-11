from django.db import models
from web_project.settings import BASE_DIR
from pathlib import Path
import uuid  


user_id = str(uuid.uuid1())
# Create your models here.
def file_name(instance, filename):
    #create the temporary path
    path  = Path.joinpath(BASE_DIR, 'data_set')
    #set the file name to the default filename "data_set.csv"
    filename = "data_set.csv"
    #return the temporary path joined with the file name
    return Path.joinpath(path, filename)

class Data_set(models.Model):
    #Add a File field to upload the files
    #and set the upload location to the return of the file_name function where the arguments are supplied by django itself
    data = models.FileField(max_length=255)
    #create for each user a unique id to reqonize wich user is visualizing which data set
    user_id = models.CharField(default= user_id, max_length=255)

