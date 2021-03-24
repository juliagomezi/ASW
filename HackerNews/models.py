from datetime import timezone, datetime

from django.db import models


# Create your models here.

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
    title = models.CharField(max_length=200, default="Oriol")
    url = models.CharField(max_length=200, default="Oriol")
    text = models.CharField(max_length=200, default="Carles")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions")

    def __str__(self):
        return self.title
