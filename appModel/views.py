
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def model(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    return render(request, 'appModel/model.html')

def predict(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    return render(request, 'appModel/predict.html')