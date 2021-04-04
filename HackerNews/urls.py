from django.urls import path

from . import views

urlpatterns = [
    path('news/', views.index, name='index'),
    path('newest/', views.newest, name='newest'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path('errormessage/', views.errormessage, name='errormessage'),
    path('item/<int:id>/', views.item, name='item'),
    path('', views.index, name='index'),
]
