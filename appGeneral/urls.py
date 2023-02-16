from django.urls import path
from . import views
#from .forms import LoginForm
#from django.contrib import admin

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginp, name = 'login'),
    path('homeLogined/', views.homeLogined, name = 'homeLogined'),
    path('logined/', views.logined, name = 'logined'),
    path('logout/', views.logoutp, name = 'logout'),
    #path('login/', views.login, {'authentication_form': LoginForm}, name = 'login'),
]