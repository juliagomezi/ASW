from datetime import timezone, datetime

from django.db import models

# Create your models here.
from django.forms import ModelForm, Textarea


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

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
    url = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
#    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class SubmitForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ['url', 'title', 'text']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
