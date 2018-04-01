# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
    Model,
    CharField,
    EmailField,
    TextField,
    BooleanField
)

# Create your models here.
class User(Model):
    nama = CharField(max_length=50, null=True)
    email = EmailField(max_length=30, null=True)
    gender = CharField(max_length=20, null=True)
    negara = CharField(max_length=20, null=True)
    kota = CharField(max_length=20, null=True)
    no_hp = CharField(max_length=12, null=True)
    univ = CharField(max_length=50, null=True)
    jurusan = CharField(max_length=50, null=True)
    ang_kuliah = CharField(max_length=5, null=True)
    ang_LMD = CharField(max_length=5, null=True)
    pekerjaan = TextField(null=True)
    instansi = CharField(max_length=30, null=True)
    aktifitas = TextField(null=True)
    tahun_aktif = CharField(max_length=20, null=True)
    verified = BooleanField(default=False)