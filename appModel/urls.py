from django.urls import path
from . import views

urlpatterns = [
    path('', views.model, name = 'modelOverview'),
    path('predict', views.predict, name = 'predict'),
    path('make_prediction_beta', views.make_prediction_beta, name = 'predict_beta'),
]