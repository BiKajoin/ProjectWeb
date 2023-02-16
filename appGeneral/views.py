from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/homeLogined')
    return render(request, 'appGeneral/home.html')

def homeLogined(request):
    if request.user.is_authenticated:
        return render(request, 'appGeneral/homeLogined.html')
    return redirect('/login')

def logined(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    return render(request, 'appGeneral/logined.html')

def loginp(request):
    if request.user.is_authenticated:
        return redirect('/logined')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)   

        user = authenticate(request, username=username, password=password)
        if user is None:
            print("error")
            context ={"error": "Invalid username or password"}
            return render(request, 'appGeneral/login.html', context)
        login(request, user)
        return redirect('/homeLogined')
    return render(request, 'appGeneral/login.html',{})

def logoutp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logout(request)
            return redirect('/')
        return render(request, 'appGeneral/logout.html',{})
    else:
        return redirect('/login')
