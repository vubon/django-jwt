# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-03 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180903_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='authorize',
            field=models.BooleanField(default=True),
        ),
    ]
