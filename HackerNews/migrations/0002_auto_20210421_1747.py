# Generated by Django 3.1.7 on 2021-04-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HackerNews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='about',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]