from django.shortcuts import render
from django.http import HttpResponse
import datetime

def home(request):
    return HttpResponse(hello_there(request,'Thymo'))
# Create your views here.
# In this file we are going to create the frontend
def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.datetime.now()
        }
    )