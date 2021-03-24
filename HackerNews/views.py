from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Contribution, User


def index(request):
    if request.method=="POST":
        id = 1
        title = request.POST["title"]
        url = request.POST["url"]
        text = request.POST["text"]
        c = Contribution(title=title, url=url, text=text, user_id=User.objects.all().first())
        c.save()
    return render(request, "news.html", {
        "contributions": Contribution.objects.all()
    })


def newest(request):
    return render(request, "newest.html", {
        "contributions": Contribution.objects.all()
    })


def submit(request):
    return render(request, "submit.html")
