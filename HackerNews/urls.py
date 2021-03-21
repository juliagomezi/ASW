from django.urls import path

from . import views

urlpatterns = [
    path('newest/', views.index, name='index'),
    path('news/', views.index, name='index'),
    path('submit/', views.submit, name='submit')
]
