from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'appGeneral/home.html')

"""def logined(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    return render(request, 'appGeneral/logined.html')"""

@login_required
def loggedin(request):
    return render(request, 'appGeneral/loggedin.html')

def loginp(request):
    if request.user.is_authenticated:
        return redirect('/loggedin')
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
        return redirect('/')
    return render(request, 'appGeneral/login.html',{})

@login_required
def logoutp(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'appGeneral/logout.html',{})
    
