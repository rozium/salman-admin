# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-23 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0028_umtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='umtoken',
            name='key',
            field=models.CharField(max_length=32),
        ),
    ]