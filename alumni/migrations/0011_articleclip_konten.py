# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-07 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0010_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleclip',
            name='konten',
            field=models.TextField(null=True),
        ),
    ]
