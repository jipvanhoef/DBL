from django.http import request
from django.shortcuts import render
from data_visualization import graph
from django_plotly_dash.dash_wrapper import DjangoDash


#This function renders our html page for the visualizations
def visualization_view(request, *args, **kwargs):
    graph.build_graph()
    #render the html file and load in the context
    return render(request, "visualizations.html", {})
    

