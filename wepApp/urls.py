from django.urls import path
from webApp import views

urlpatterns = [
    path("", views.home, name="home"),
]