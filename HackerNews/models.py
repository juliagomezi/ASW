from django.db import models


# Create your models here.

class User(models.Model):
    id = models.IntegerField
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
    id = models.IntegerField
    content = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
