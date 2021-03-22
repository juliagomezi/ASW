from django.urls import path

from . import views

urlpatterns = [
    path('news/', views.index, name='index'),
    path('newest/', views.newest, name='newest'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path("add", views.add, name="add"),
    path('', views.index, name='index'),
]
