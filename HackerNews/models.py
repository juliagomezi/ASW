from datetime import timezone, datetime

from django.db import models

from django.core.exceptions import ValidationError
# Create your models here.
from django.forms import ModelForm, Textarea, TextInput, URLInput
from django.contrib.auth.models import User
from django import forms


class Contribution(models.Model):
    URL = 'url'
    ASK = 'ask'
    CHOICES = [
        (URL, 'url'),
        (ASK, 'ask')
    ]
    type = models.CharField(
        max_length=3,
        choices=CHOICES,
        default='url')
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    points = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE, related_name="comments")
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text


class ContributionVote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)


class CommentVote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class SubmitForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ['url', 'title', 'text']
        widgets = {
            'url': URLInput(attrs={'size': 50}),
            'title': TextInput(attrs={'size': 50, 'required': False}),
            'text': Textarea(attrs={'cols': 49, 'rows': 4, 'required': False}),
        }

    def clean(self):
        super(SubmitForm, self).clean()
        cd = self.cleaned_data

        url = cd.get('url')
        text = cd.get('text')

        if not url and not text:
            raise ValidationError("FORMINCOMPLET")

        return cd


class DetailForm(forms.Form):
    about = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': '60', 'rows': '5'}))
    show_dead = forms.BooleanField(required=False)
    no_procrast = forms.BooleanField(required=False)
    max_visit = forms.IntegerField(min_value=0)
    min_away = forms.IntegerField(min_value=0)
    delay = forms.IntegerField(min_value=0)


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    karma = models.IntegerField(default=0)
    about = models.CharField(max_length=200, default="", blank=True)
    created = models.DateTimeField(default=datetime.now)
    show_dead = models.BooleanField(default=False)
    no_procrast = models.BooleanField(default=False)
    max_visit = models.PositiveIntegerField(default=20)
    min_away = models.PositiveIntegerField(default=180)
    delay = models.PositiveIntegerField(default=0)

    def set_data(self, detail_form: DetailForm):
        self.about = detail_form.cleaned_data['about']
        self.show_dead = detail_form.cleaned_data['show_dead']
        self.no_procrast = detail_form.cleaned_data['no_procrast']
        self.max_visit = detail_form.cleaned_data['max_visit']
        self.min_away = detail_form.cleaned_data['min_away']
        self.delay = detail_form.cleaned_data['delay']
