# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-23 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0008_auto_20170223_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='overs',
            field=models.IntegerField(default=1),
        ),
    ]
