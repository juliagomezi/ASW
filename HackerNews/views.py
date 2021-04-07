from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

from HackerNews.models import Contribution, SubmitForm

from .models import Contribution


def index(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all(),
        "submit": False
    })


def newest(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "newest"
    })


def threads(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "threads"
    })


def ask(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "ask",
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
                return errormessage(request)  # SI JA EXISTEIX S'HA D'ANAR A LA PAG DE LA CONTRIBUCIO
            form.save()
            return index(request)
        return errormessage(request)


def errormessage(request):
    return render(request, "message.html")


def signout(request):
    logout(request)
    return redirect('/')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):

        creationForm = UserCreationForm(prefix='creation')
        creationForm.fields['username'].required = False
        creationForm.fields['password1'].required = False
        creationForm.fields['password2'].required = False
        loginForm = AuthenticationForm(prefix='login')
        loginForm.fields['username'].required = False
        loginForm.fields['password'].required = False

        return self.render_to_response(
            {'c_form': creationForm, 'a_form': loginForm})

    def post(self, request, *args, **kwargs):
        creationForm = UserCreationForm(request.POST, prefix='creation')
        form = AuthenticationForm(request.POST, prefix='login')
        if 'creation' in request.POST and creationForm.is_bound and creationForm.is_valid():
            creationForm.save()
            user = creationForm.cleaned_data['username']
            password = creationForm.cleaned_data['password1']
            user = authenticate(request, username=user, password=password)
            login(request, user)
            return redirect('/')
        elif 'login' in request.POST:
            username = request.POST['login-username']
            password = request.POST['login-password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

        return self.render_to_response({'c_form': creationForm, 'a_form': AuthenticationForm(prefix='login')})
