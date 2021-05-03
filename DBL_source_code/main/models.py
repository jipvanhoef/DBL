from django.db import models
from web_project.settings import BASE_DIR
from pathlib import Path

# Create your models here.
class Data_set(models.Model):
    data = models.FileField(upload_to = Path.joinpath(BASE_DIR, 'data_set'))