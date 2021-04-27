from django.shortcuts import render


#This function renders our html page for the visualizations
def visualization_view(request, *args, **kwargs):
    return render(request, "visualizations.html", {})