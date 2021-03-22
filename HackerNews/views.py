from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from HackerNews.models import Contribution, User


def index(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all()
    })


def newest(request):
    return render(request, "newest.html")


# class SubmitView(generic.DetailView):
#     template_name = "submit.html"
#     model = Contribution
# view for the product entry page
class SubmitView(CreateView):
    model = Contribution
    fields = ['text', 'url', 'title']


def submit(request):
    return render(request, "submit.html")


def add(request):
    return render(request, "submit.html")
