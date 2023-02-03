
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def model(request):
    return render(request, 'appModel/model.html')