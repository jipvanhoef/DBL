from django.shortcuts import render
from .forms import Data_setForm

from web_project.settings import BASE_DIR

from pathlib import Path

import uuid    

import os

#In this file are the functions to render our pages and load the content
#create for each user a unique id to reqonize wich user is visualizing which data set
user_id = str(uuid.uuid1()) 

#This function renders our html page for the home page
def home_view(request, *args, **kwargs):
    return render(request, "index.html",{})

#This function renders our html page for the data input
def data_input_view(request, *args, **kwargs):
    #check the request method 
    if request.method == "POST":
        #Initilize the form in the varible form
        form = Data_setForm(request.POST, request.FILES)

        #check if the form is valid
        if form.is_valid():

            #summit the form
            data = form.save()
            #create the root varible from the main folder with the data sets
            root = Path.joinpath(BASE_DIR, "data_set")
            #create a new path for the user using their unique id
            user_folder = Path.joinpath(root, user_id)
            #create a new folder at the user_folder path
            os.mkdir(user_folder)

            #The path where their summitted file is temporarly stored
            original_path = Path.joinpath(BASE_DIR, "data_set/data_set.csv")

            #The new path where their summitted file is stored
            new_path = Path.joinpath(BASE_DIR, "data_set/" + user_id + "/data_set.csv")

            #Put the their file in their user folder
            os.rename(original_path,new_path)
    else:
        #set the form to a empty Data_setForm
        form = Data_setForm() 

    #set the html context to the form      
    context = {'form': form}

    #render the html page with the context
    return render(request, "data_input.html", context)

        
#This function renders our html page for the contact page
def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


