from django.urls import path, re_path

from . import views

urlpatterns = [
    path('newest/', views.newest, name='newest'),
    path('threads/', views.threads, name='threads'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.signout, name='logout'),
    path('user/<int:id>', views.ask, name='user'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path('errormessage/', views.errormessage, name='errormessage'),
    path('item/<int:id>/', views.item, name='item'),
    path('', views.index, name='index'),
]
