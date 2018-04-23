# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, binascii
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import (
    Model,
    CharField,
    EmailField,
    TextField,
    BooleanField,
    FileField,
    AutoField,
    DecimalField,
    ImageField,
    ManyToManyField,
    OneToOneField,
    PositiveIntegerField,
    DateTimeField,
    CASCADE,
)


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

# Create your models here.
class User(Model):
    nama = CharField(max_length=50, null=True)
    email = EmailField(max_length=30, null=True)
    gender = CharField(max_length=20, null=True)
    alamat = CharField(max_length=100, null=True)
    negara = CharField(max_length=20, null=True)
    kota = CharField(max_length=20, null=True)
    no_hp = CharField(max_length=12, null=True)
    univ = CharField(max_length=50, null=True)
    jurusan = CharField(max_length=50, null=True)
    ang_kuliah = CharField(max_length=5, null=True)
    ang_LMD = CharField(max_length=5, null=True)
    pekerjaan = CharField(max_length=50, null=True)
    instansi = CharField(max_length=30, null=True)
    aktifitas = TextField(null=True)
    tahun_aktif = TextField(null=True)
    verified = BooleanField(default=False)
    password = CharField(max_length=50, null=True)
    # edited 15 april
    latitude = DecimalField(max_digits=20, decimal_places=15, null=True)
    longitude = DecimalField(max_digits=20, decimal_places=15, null=True)
    pertanyaan1 = TextField(null=True)
    pertanyaan2 = TextField(null=True)
    jawaban1 = TextField(null=True)
    jawaban2 = TextField(null=True)
    profile_image = ImageField(upload_to=get_image_path, blank=True, null=True)

class ArticleClip(Model):
    #attributes
    @property
    def article_id(self):
        return self.id
    judul = CharField(max_length=100, null=True)
    deskripsi = TextField(null=True)
    konten = TextField(null=True)
    thumbnail = ImageField(upload_to='article-thumbnails/', default='article-thumbnails/not-available.jpg')
    
    liked = ManyToManyField(User)
    like_count = PositiveIntegerField(default=0)
    view_count = PositiveIntegerField(default=0)

    published = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

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


class Token(Model):

    key = CharField(_("Key"), max_length=40, primary_key=True)

    user = OneToOneField(
        User, related_name='auth_token',
        on_delete=CASCADE, verbose_name="User"
    )
    created = DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(MyOwnToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key