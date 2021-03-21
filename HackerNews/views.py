from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "news.html")

def submit(request):
    return render(request, "submit.html")
