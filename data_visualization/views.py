from django.http import request, response
from django.shortcuts import render
from data_visualization import graph
from django_plotly_dash.dash_wrapper import DjangoDash
from main.models import User
from .models import user_id


#This function renders our html page for the visualizations
def visualization_view(request, *args, **kwargs):
    graph.build_graph()
    try:
        User.objects.get(user_id = user_id)
    except:
        User.objects.create(user_id = user_id)
        return response.HttpResponseRedirect('/tour/')
    #render the html file and load in the context
    return render(request, "visualizations.html", {})

def visualization_view_tour(request, *args, **kwargs):
    return render(request, "tour_visualizations.html", {})

