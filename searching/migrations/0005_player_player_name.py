# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-28 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0004_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='player_name',
            field=models.CharField(default='NO NAME GIVEN', max_length=50),
        ),
    ]
