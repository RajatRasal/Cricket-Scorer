# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-23 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0009_match_overs'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='result',
            field=models.CharField(default='x', max_length=50),
        ),
    ]