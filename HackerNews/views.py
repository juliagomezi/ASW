from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import  TemplateView

from HackerNews.models import Contribution, User, SubmitForm


from .models import Contribution, User


def index(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all().order_by('points')
    })


def newest(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all().order_by('-date')
    })


class SubmitView(TemplateView):
    template_name = "submit.html"

    def get(self, request):
        form = SubmitForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SubmitForm(request.POST)
        if form.is_valid():
            form.save()

        return index(request)
