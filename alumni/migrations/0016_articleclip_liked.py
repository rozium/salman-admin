# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-18 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0015_auto_20180415_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleclip',
            name='liked',
            field=models.ManyToManyField(to='alumni.User'),
        ),
    ]
