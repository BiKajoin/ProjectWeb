
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def model(request):
    return render(request, 'appModel/model.html')

@login_required
def predict(request):
    return render(request, 'appModel/predict.html')