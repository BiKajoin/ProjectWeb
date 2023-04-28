from django.urls import path
from . import views

urlpatterns = [
    path('', views.model, name = 'modelOverview'),
    path('predict', views.predict, name = 'predict'),
    path('makePrediction', views.makePrediction, name = 'makePrediction'),

    path('testPrediction', views.testPrediction, name = 'testPrediction'),
]