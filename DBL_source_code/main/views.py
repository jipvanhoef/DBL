from django.shortcuts import render
from .forms import Data_setForm
#In this file are the functions to render our pages and load the content

#This function renders our html page for the home page
def home_view(request, *args, **kwargs):
    return render(request, "index.html",{})

#This function renders our html page for the data input
def data_input_view(request, *args, **kwargs):
    if request.method == "POST":
        form = Data_setForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = Data_setForm()       
    context = {'form': form}
    return render(request, "data_input.html", context)

        
#This function renders our html page for the contact page
def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


