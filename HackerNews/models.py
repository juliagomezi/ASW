from datetime import timezone, datetime

from django.db import models

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
    url = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    points = models.IntegerField(default=0)
#    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SubmitForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ['url', 'title', 'text']
        widgets = {
            'url': URLInput(attrs={'size': 50}),
            'title': TextInput(attrs={'size': 50}),
            'text': Textarea(attrs={'cols': 49, 'rows': 4}),
        }
