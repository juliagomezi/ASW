from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

from HackerNews.models import Contribution, User, SubmitForm

from .models import Contribution, User


def index(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all(),
        "submit": False
    })


def newest(request):
    return render(request, "newest.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "newest"
    })


def threads(request):
    return render(request, "newest.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "threads"
    })


def ask(request):
    user = User()
    user.id = 123
    user.name = "Reus>Tgn"
    return render(request, "newest.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "ask",
        "logged": True,
        "user": user,
    })


def item(request, id):
    return render(request, "item.html")


def item(request, id):
    return render(request, "item.html")


class SubmitView(TemplateView):
    template_name = "submit.html"

    def get(self, request):
        form = SubmitForm
        return render(request, self.template_name, {"form": form, "submit": True})

    def post(self, request):
        form = SubmitForm(request.POST)
        url = request.POST.get('url')
        if form.is_valid():
            match = Contribution.objects.filter(url=url).exists()
            if match:
                return errormessage(request) #SI JA EXISTEIX S'HA D'ANAR A LA PAG DE LA CONTRIBUCIO
            form.save()
            return index(request)
        return errormessage(request)



def errormessage(request):
    return render(request, "message.html")
