from django.urls import path
from . import views

urlpatterns = [
    path('', views.model, name = 'modelOverview'),
    path('predict', views.predict, name = 'predict'),
]