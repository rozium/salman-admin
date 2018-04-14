# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.core.serializers import serialize
from .models import User, Counter, LazyEncoder, SummernoteForm, About, ArticleClip
# from .auth import UserAuthentication
from rest_framework import viewsets

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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
    EmailSerializer,
)

############# Index ##################

def index(request):
    if request.user.is_authenticated:
        return redirect("/menyapa/list/")
    else:
        return redirect("/login/")

############# About ##################

def about(request):
    if request.user.is_authenticated:
        about = About.objects.all()[:1].get()
        context = {'about': about}
        return render(request, 'about.html', context)
    else:
        return redirect("/login/")

############# Verifikasi ##################

def verifikasi(request):
    if request.user.is_authenticated:
        users = User.objects.only("nama","email").filter(verified=False)
        context = {'users': users, 'counter': Counter()}
        return render(request, 'verifikasi.html', context)
    else:
        return redirect("/login/")

def verifuser(request):
    if request.user.is_authenticated:
        email = request.GET.get('email', None)
        data = {
            'users' : serialize('json', User.objects.filter(email=email))
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Error!'})

def verifconfirm(request):
    if request.user.is_authenticated:
        email = request.GET.get('email', None)

        user = User.objects.filter(email=email).update(verified=True)

        data = {
            'msg' : 'Akun berhasil diverifikasi!'
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Error!'})

############# Menyapa ##################

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


###################################################
####################### API #######################
###################################################

############# About ##################

class AboutView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
    	data = {
    		'data': AboutSerializer(About.objects.all(), many=True).data[0],
    		'success': True,
    		'error': None
    	}

    	return Response(data)

############# User ##################

class UserCreateView(CreateAPIView):
    serializer_class = CreateSeliazier
    queryset = User.objects.all()

class EmailLoginView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = EmailSerializer(data=data)
        
        if serializer.is_valid():
            new_data = serializer.data
            return Response({
                'data' : new_data,
                'error' : None,
                'success' : True
            })
        return Response({
            'data' : None,
            'error' : {
                'code': 401,
                'message': serializer.errors.values()[0][0],
            },
            'success' : False,
        })

class UserLoginView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            new_data = serializer.data
            # return Response(new_data, status=HTTP_200_OK)
            return Response({
                'data' : new_data,
                'error' : None,
                'success' : True
            })
        return Response({
            'data' : None,
            'error' : {
                'code': 401,
                'message': serializer.errors.values()[0][0],
            },
            'success' : False,
        })


# 8b6bc5d8046c8466359d3ac43ce362ab