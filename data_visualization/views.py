from django.http import request
from django.shortcuts import render
from django.urls.conf import path
from django_plotly_dash.dash_wrapper import DjangoDash


#This function renders our html page for the visualizations
def visualization_view(request, *args, **kwargs):
    #render the html file and load in the context
    return render(request, "visualizations.html", {})
    

