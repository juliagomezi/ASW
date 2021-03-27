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


# class SubmitView(generic.DetailView):
#     template_name = "submit.html"
#     model = Contribution
# view for the product entry page
class SubmitView(TemplateView):
    template_name = "submit.html"

    def get(self, request):
        form = SubmitForm
        return render(request, self.template_name, {"form": form, "submit": True})

    def post(self, request):
        form = SubmitForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/index/', request)
