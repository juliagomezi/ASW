# Generated by Django 3.1.7 on 2021-04-11 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HackerNews', '0002_auto_20210411_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='father',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HackerNews.comment'),
        ),
    ]