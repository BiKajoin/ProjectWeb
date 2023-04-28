from django.urls import path
from . import views

urlpatterns = [
    path('', views.data, name = 'data'),
    path('upload/', views.upload, name = 'upload'),
    path('success/', views.success_page, name='success'),
    path('fail/', views.fail_page, name='fail'),
    path('drop-collection/', views.drop_collection, name='drop-collection'),
]