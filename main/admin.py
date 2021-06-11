from django.contrib import admin

from data_visualization.models import Data_set
from .models import User
# Register your models here.

admin.site.register(Data_set)
admin.site.register(User)