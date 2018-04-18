# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from .models import User, Counter, LazyEncoder, About, ArticleClip

from ast import literal_eval

from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
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
    CreateSeliazier,
    LoginSerializer,
    EmailSerializer,
    UpdateSerializer,
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

def aboutsave(request):
    if request.user.is_authenticated:
        text_about = request.POST.get('text_about', None)
        text_alamat = request.POST.get('text_alamat', None)
        text_no_hp = request.POST.get('text_no_hp', None)
        text_email = request.POST.get('text_email', None)
        if text_about and text_alamat and text_no_hp and text_email:
            About.objects.filter(pk=1).update(text_about=text_about, text_alamat=text_alamat, text_no_hp=text_no_hp, text_email=text_email)
            data = {
                'msg' : 'About berhasil disimpan'
            }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Error!'})

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
        context = {'article' : articleClips}
        return render(request, 'menyapa_edit.html', context)
    else:
        return redirect("/login/")

def menyapaEditSave(request):
    if request.user.is_authenticated:
        id = request.POST.get('id', None)
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        content = content.replace("'", "\\'")
        # photo_url = request.POST.get('photo_url', None)
        # articleClips = ArticleClip.objects.get(id = article_id)
        if id and title and content:
            ArticleClip.objects.filter(pk=id).update(judul=title, konten=content)
        return redirect("/menyapa/list/")
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
            'data': About.objects.all().filter(pk=1).values("text_email", "text_alamat", "text_no_hp", "text_about")[0],
            'success': True,
            'error': None,
        }

        return Response(data)

############# User ##################

class UserCreateView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = CreateSeliazier

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateSeliazier(data=data)
        
        if serializer.is_valid():
            new_data = serializer.validated_data
            new_data = serializer.save()
            return Response({
                'data' : {
                    'email': new_data.email,
                    'token': "tokenpalsuhehe",
                    'verified': False,
                    'id': new_data.id,
                },
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

class GetUserView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(Q(pk=int(self.kwargs['id'])))
        if user.exists():
            img = user.values('profile_image')[0]["profile_image"]
            if img:
                img = "http://" + request.get_host() + '/media/' + img
            else:
                img = None
            data = {
                'data' : {
                    'id' : user.values('id')[0]["id"],
                    'nama' : user.values('nama')[0]["nama"],
                    'email' : user.values('email')[0]["email"],
                    'gender' : user.values('gender')[0]["gender"],
                    'alamat' : user.values('alamat')[0]["alamat"],
                    'negara' : user.values('negara')[0]["negara"],
                    'kota' : user.values('kota')[0]["kota"],
                    'no_hp' : user.values('no_hp')[0]["no_hp"],
                    'univ' : user.values('univ')[0]["univ"],
                    'jurusan' : user.values('jurusan')[0]["jurusan"],
                    'ang_kuliah' : user.values('ang_kuliah')[0]["ang_kuliah"],
                    'ang_LMD' : user.values('ang_LMD')[0]["ang_LMD"],
                    'pekerjaan' : user.values('pekerjaan')[0]["pekerjaan"],
                    'instansi' : user.values('instansi')[0]["instansi"],
                    'aktifitas' : literal_eval(user.values('aktifitas')[0]["aktifitas"]),
                    'tahun_aktif' : literal_eval(user.values('tahun_aktif')[0]["tahun_aktif"]),
                    'profile_image' : img,
                    'latitude' : user.values('latitude')[0]["latitude"],
                    'longitude' : user.values('longitude')[0]["longitude"],
                },
                'success': True,
                'error': None,
            }
            return Response(data)
        else:
            data = {
                'data': None,
                'success': False,
                'error': {
                    'code': 401,
                    'message': "User tidak ditemukan",
                },
            }
            return Response(data)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UpdateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UpdateSerializer(data=data)
        if serializer.is_valid():
            return Response({
                'data' : {'msg': 'Akun berhasil diupdate'},
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

class SearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', None)

        if not query:
            success = False
            value = None
            error = {'code': 401,'message': "Missing parameter ?q="}
        else:
            success = True
            error = None
            value = User.objects.all().filter(Q(nama__contains=query) | Q(kota__contains=query)).values('nama', 'email', 'kota', 'profile_image')

        data = {
            'data': value,
            'success': success,
            'error': error,
        }

        return Response(data)

############# Menyapa ##################

class MenyapaDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', None)
        value = ArticleClip.objects.all().filter(Q(pk=query))
        if not query:
            success = False
            value = None
            error = {'code': 401,'message': "Missing parameter ?q="}
        elif not value:
            success = False
            value = None
            error = {'code': 401,'message': "Artikel tidak ditemukan."}
        else:
            success = True
            error = None
            value = value.values()
            value = value[0]

        data = {
            'data': value,
            'success': success,
            'error': error,
        }

        return Response(data)

class MenyapaView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):

        data = {
            'data': ArticleClip.objects.all().values()[0:3],
            'success': True,
            'error': None,
        }

        return Response(data)

# 8b6bc5d8046c8466359d3ac43ce362ab