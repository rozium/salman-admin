# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.serializers import serialize
from .models import User, Counter, LazyEncoder, SummernoteForm, About
from rest_framework import viewsets
from alumni.serializers import AboutSerializer

def index(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    else:
        return redirect("/login/")

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {})
    else:
        return redirect("/login/")

def about(request):
    if request.user.is_authenticated:
        about = About.objects.all()[:1].get()
        context = {'about': about}
        return render(request, 'about.html', context)
    else:
        return redirect("/login/")
        
def verifikasi(request):
    if request.user.is_authenticated:
        users = User.objects.all().filter(verified=False)
        context = {'users': users, 'usersJSON': serialize('json', User.objects.all().filter(verified=False), cls=LazyEncoder), 'counter': Counter()}
        return render(request, 'verifikasi.html', context)
    else:
        return redirect("/login/")

def menyapaEdit(request):
    if request.user.is_authenticated:
        context = {'form': SummernoteForm()}
        return render(request, 'menyapa_edit.html', context)
    else:
        return redirect("/login/")

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer  