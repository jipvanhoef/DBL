from django.shortcuts import render
from .forms import Data_setForm

from web_project.settings import BASE_DIR

from pathlib import Path

import uuid    

import os

#In this file are the functions to render our pages and load the content
user_id = str(uuid.uuid1()) 

#This function renders our html page for the home page
def home_view(request, *args, **kwargs):
    return render(request, "index.html",{})

#This function renders our html page for the data input
def data_input_view(request, *args, **kwargs):
    if request.method == "POST":
        form = Data_setForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()

            root = Path.joinpath(BASE_DIR, "data_set")

            user_folder = Path.joinpath(root, user_id)

            os.mkdir(user_folder)

            original_path = Path.joinpath(BASE_DIR, "data_set/data_set.csv")
            new_path = Path.joinpath(BASE_DIR, "data_set/" + user_id + "/data_set.csv")

            os.rename(original_path,new_path)
    else:
        form = Data_setForm()       
    context = {'form': form}
    return render(request, "data_input.html", context)

        
#This function renders our html page for the contact page
def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


