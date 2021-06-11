from django.db import models
from data_visualization.models import user_id

class User(models.Model):
    user_id = models.CharField(default= user_id, max_length= 255)

