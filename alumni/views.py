# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from .models import User

def index(request):
    if request.user.is_authenticated:
        return redirect("/verifikasi/")
    else:
        return redirect("/login/")

def home(request):
    return render(request, 'home.html', {})

def verifikasi(request):
    users = User.objects.all()
    context = {'users': users, 'usersJSON': serialize('json', User.objects.all(), cls=LazyEncoder)}
    return render(request, 'verifikasi.html', context)

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)