# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.serializers import serialize
from .models import User, Counter, LazyEncoder, SummernoteForm, About, ArticleClip
from .auth import UserAuthentication
from rest_framework import viewsets, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from alumni.serializers import (
    AboutSerializer, 
    CreateSeliazier,
    LoginSerializer,
)

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

def menyapaEdit(request, article_id):
    if request.user.is_authenticated:
        articleClips = ArticleClip.objects.get(id = article_id)
        context = {'form': SummernoteForm(), 'article' : articleClips}
        return render(request, 'menyapa_edit.html', context)
    else:
        return redirect("/login/")

def menyapaList(request):
    if request.user.is_authenticated:
        articleClips = ArticleClip.objects.all()
        context = {'articleClips': articleClips}
        return render(request, 'menyapa_list.html', context)
    else:
        return redirect("/login/")

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer  

class UserCreateView(CreateAPIView):
    serializer_class = CreateSeliazier
    queryset = User.objects.all()

class UserLoginView(APIView):
    authentication_classes = (UserAuthentication,)
    def post(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)
