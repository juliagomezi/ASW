from django.urls import path, re_path

from . import views

urlpatterns = [
    path('news/', views.index, name='index'),
    path('newest/', views.newest, name='newest'),
    path('threads/', views.threads, name='threads'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.ask, name='login'),
    path('user/<int:id>', views.ask, name='user'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path('', views.index, name='index'),
]
