from django.contrib import admin

# Register your models here.

from .models import Contribution, Comment, Point

admin.site.register(Contribution)
admin.site.register(Comment)
admin.site.register(Point)