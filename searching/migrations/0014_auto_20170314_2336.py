# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-14 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0013_auto_20170314_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
