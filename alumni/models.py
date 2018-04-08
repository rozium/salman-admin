# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.db.models import (
    Model,
    CharField,
    EmailField,
    TextField,
    BooleanField,
    FileField,
    AutoField
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
    password = CharField(max_length=50, null=True)

class ArticleClip(Model):
    #attributes
    @property
    def article_id(self):
        return self.id
    judul = CharField(max_length=100, null=True)
    deskripsi = TextField(null=True)
    konten = TextField(null=True)
    thumbnail = FileField(upload_to='article-thumbnails/')

class About(Model):
    text_about = TextField(null=True)
    text_alamat = CharField(max_length=100, null=True)
    text_no_hp = CharField(max_length=40, null=True)
    text_email = EmailField(max_length=30, null=True)

class Counter:
    counter = 1
    def inc(self):
        self.counter += 1
    def dec(self):
        self.counter -= 1

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)

class SummernoteForm(forms.Form):
    foo = forms.CharField(widget=SummernoteWidget(), label='')