from django.urls import path
from . import views
#from .forms import LoginForm
#from django.contrib import admin

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginp, name = 'login'),
    path('loggedin/', views.loggedin, name = 'loggedin'),
    path('logout/', views.logoutp, name = 'logout'),
]

handler404 = 'appGeneral.views.handle404'
