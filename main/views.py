import uuid
from django.core.exceptions import ValidationError
from django.http import response
from main.models import Data_set
from django.shortcuts import redirect, render
from .forms import Data_setForm
from .models import user_id

from web_project.settings import BASE_DIR

from pathlib import Path


from data_visualization import graph
import os

import datetime
from main.forms import Data_setForm
from main.models import User

#In this file are the functions to render our pages and load the content


#This function renders our html page for the home page
tour = True
tour_in_progress = False
def home_view(request, *args, **kwargs):
    try:
        User.objects.get(user_id = user_id)
        if not tour_in_progress:
            tour = False
    except:
        User.objects.create(user_id = user_id)
        tour = True
        

    if tour:
        template = "index_tour.html"
    else:
        template = 'index.html'
    return render(request, template,{})

def start_tour(request):
    tour_in_progress = True
    response = redirect('/data_input/')
    return response

#This function renders our html page for the data input
def data_input_view(request, *args, **kwargs):
    #check if there are files that are stored to long and delete them
    clean_unused_data()
    #check the request method 
    if request.method == "POST":
        #Initilize the form in the varible form
        form = Data_setForm(request.POST, request.FILES)

        #check if the form is valid
        if form.is_valid():
            #summit the form
            form.save()
            graph.build_graph()
            badinput_error = False
        else:
            badinput_error = True
    else:
        #set the form to a empty Data_setForm
        form = Data_setForm()
        badinput_error = False 

    #set the html context to the form      
    context = {'form': form, 'badinput_flag': badinput_error}

    #render the html page with the context
    return render(request, "data_input.html", context)

def clean_unused_data():
    experiation_time = datetime.timedelta(hours= 2)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    data_sets = Data_set.objects.all()
    for entry in data_sets:
        start_time = entry.time
        diff = (start_time - current_time)
        if( diff > experiation_time):
            delete_folder(path= entry.file.path)
            entry.delete()

def delete_folder(path):
    try:
        path = Path(path)
        path.unlink()
        directory = os.path.dirname(path)
        directory = Path(directory)
        directory.rmdir()
    except:
        print(os.error)


        
#This function renders our html page for the contact page
def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


