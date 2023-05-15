

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homer(Request):
    return HttpResponse('<h1> Water Home</h1>')
def home(request):
    return render(request, 'sms/sample_home.html')