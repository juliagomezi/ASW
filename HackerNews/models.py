from datetime import timezone, datetime

from django.db import models

from django.core.exceptions import ValidationError
# Create your models here.
from django.forms import ModelForm, Textarea, TextInput, URLInput


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name


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
    points = models.IntegerField(default=0)
#    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class SubmitForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ['url', 'title', 'text']
        widgets = {
            'url': URLInput(attrs={'size': 50}),
            'title': TextInput(attrs={'size': 50,'required': False}),
            'text': Textarea(attrs={'cols': 49, 'rows': 4,'required': False}),
        }

    def clean(self):
        super(SubmitForm, self).clean()
        cd = self.cleaned_data

        url = cd.get('url')
        text = cd.get('text')

        if not url and not text:

            raise ValidationError("FORMINCOMPLET")

        return cd

