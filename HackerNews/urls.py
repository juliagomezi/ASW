from django.urls import path

from . import views

urlpatterns = [
    path('news/', views.index, name='index'),
    path('newest/', views.newest, name='newest'),
    path('submit/', views.submit, name='submit'),
    path('', views.index, name='index'),
]
