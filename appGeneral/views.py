from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'appGeneral/home.html')

def login(request):
    return render(request, 'appGeneral/login.html')