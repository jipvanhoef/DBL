"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url


from main.views import home_view, data_input_view, contact_view
from main.views import home_view_tour, data_input_view_tour, contact_view_tour
from data_visualization.views import visualization_view
from data_visualization.views import visualization_view_tour
from data_visualization import graph

#This are the url patterns the first argument in path() is the suffix of our normal url like this "ourwebpage/suffix.com"
#The second argument is the imported view function to render our html  
#The third argument is the internal name of the url this can be used to link the urls to eachother in the html files
urlpatterns = [
    path('',home_view, name = 'home'),
    path('tour/', home_view_tour, name = "tour"),

    path('data_input/', data_input_view, name = "data_input" ),
    path('data_input/tour/', data_input_view_tour, name = "data_input_tour" ),

    path('visualization/', visualization_view, name = 'visualization'),
    path('visualization/tour', visualization_view_tour, name = 'visualization_tour'),

    path('contact/', contact_view, name = "contact"),
    path('contact/tour', contact_view_tour, name = "contact_tour"),

    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
