from django.db import models
from web_project.settings import BASE_DIR
from pathlib import Path


# Create your models here.
def file_name(instance, filename):
    path  = Path.joinpath(BASE_DIR, 'data_set')
    filename = "data_set.csv"
    return Path.joinpath(path, filename)

class Data_set(models.Model):
    data = models.FileField(upload_to = file_name)

