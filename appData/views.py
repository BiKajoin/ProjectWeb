from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def data(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    return render(request, 'appData/data.html')
