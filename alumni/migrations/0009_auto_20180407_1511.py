# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-07 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0008_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleClip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=100, null=True)),
                ('deskripsi', models.TextField(null=True)),
                ('thumbnail', models.FileField(upload_to='article-thumbnails/')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]
