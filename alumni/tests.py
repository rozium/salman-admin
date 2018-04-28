# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from calendar import timegm
from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Q
from ast import literal_eval
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,ArticleClip,About,UmToken
from django.core.serializers import serialize
from alumni.serializers import LoginSerializer
import json

host = 'testserver'
client = Client()
# Create your tests here.
class ArticleClipTestCase(TestCase):
    def setUp(self):
        ArticleClip.objects.create(
            judul = 'Test',
            deskripsi = 'Deskripsi',
            konten = 'Konten',
            like_count = 10,
            view_count = 10,
            published = True,
            pinned = True,
        )
    def test_article_clip_get_all(self):
        response = client.get(reverse('api_menyapa'))

        artikels = ArticleClip.objects.filter(published=True).order_by('-pinned', '-created_at').values()

        for artikel in artikels:

            # img thing
            img = artikel["thumbnail"]
            if img:
                img = "http://" + host + '/media/' + img
            else:
                img = None
            artikel["thumbnail"] = img

            # date thing
            created = str(artikel["created_at"])
            utc_time_create = time.strptime(str(artikel["created_at"]), "%Y-%m-%d %H:%M:%S.%f+00:00")
            utc_time_update = time.strptime(str(artikel["updated_at"]), "%Y-%m-%d %H:%M:%S.%f+00:00")

            artikel["created_at"] = timegm(utc_time_create)
            artikel["updated_at"] = timegm(utc_time_update)

            # konten thing
            artikel["konten"] = "http://" + host + "/menyapa/page/?q=" + str(artikel["id"])

        data = {
            'data': artikels,
            'success': True,
            'error': None,
        }
        
        self.assertEqual(response.data['data'].values('konten')[0]['konten'],data['data'].values('konten')[0]['konten'])
        self.assertEqual(response.data['data'].values('judul')[0]['judul'],data['data'].values('judul')[0]['judul'])
        self.assertEqual(response.data['data'].values('deskripsi')[0]['deskripsi'],data['data'].values('deskripsi')[0]['deskripsi'])
        self.assertEqual(response.data['data'].values('id')[0]['id'],data['data'].values('id')[0]['id'])
        self.assertEqual(response.data['data'].values('thumbnail')[0]['thumbnail'],data['data'].values('thumbnail')[0]['thumbnail'])
        self.assertEqual(response.data['data'].values('like_count')[0]['like_count'],data['data'].values('like_count')[0]['like_count'])
        self.assertEqual(response.data['data'].values('view_count')[0]['view_count'],data['data'].values('view_count')[0]['view_count'])
        self.assertEqual(response.data['data'].values('published')[0]['published'],data['data'].values('published')[0]['published'])
        self.assertEqual(response.data['data'].values('pinned')[0]['pinned'],data['data'].values('pinned')[0]['pinned'])
        self.assertEqual(response.data['data'].values('created_at')[0]['created_at'],data['data'].values('created_at')[0]['created_at'])
        self.assertEqual(response.data['data'].values('updated_at')[0]['updated_at'],data['data'].values('updated_at')[0]['updated_at'])
        
        
class AboutTestCase(TestCase):
    def setUp(self):
        About.objects.create(
            text_about = 'About',
            text_alamat = 'Alamat',
            text_no_hp = 'No HP',
            text_email = 'Email'
        )

    def test_api_about(self):
        #get API Response
        response = client.get(reverse('api_about'))
        # get data from db
        data = {
            'data': About.objects.filter(pk=1).values("text_email", "text_alamat", "text_no_hp", "text_about")[0],
            'success': True,
            'error': None,
        }

        self.assertEqual(response.data,data)

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            nama = 'Nama',
            email = 'Email@gmail.com',
            gender = 'Gender',
            alamat = 'Alamat',
            negara = 'Negara',
            kota = 'Kota',
            no_hp = 'HP',
            univ = 'Univ',
            jurusan = 'Jurusan',
            ang_kuliah = '12',
            ang_LMD = '12',
            pekerjaan = 'pekerjaan',
            instansi = 'instansi',
            aktifitas = '["aktifitas"]',
            tahun_aktif = '["tahun_aktif"]',
            verified = True,
            password = 'password',
            latitude = 1.0,
            longitude = 1.0,
            pertanyaan1 = 'asd',
            pertanyaan2 = 'asd',
            jawaban1 = 'asd',
            jawaban2 = 'asd'
        )

        self.payload = {
            'email' : 'Email@gmail.com',
            'password' : 'password'
        }

        


    def test_api_login_logout(self):
        response = client.post(
            reverse('api_login'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertTrue(response.data['success'])
        token = response.data['data']['token']
        header = {'HTTP_UM' : token}
        logout_response = client.post(reverse('api_logout'),content_type='application/json',**header)
        self.assertTrue(response.data['success'])

    def test_api_login_gagal(self):
        payload = {
            'email' : 'Email31@gmail.com',
            'password' : 'password'
        } 
        response = client.post(
            reverse('api_login'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertFalse(response.data['success'])


    def test_api_register(self):
        payload = {
            'nama' : 'Nama',
            'email' : 'Email2@gmail.com',
            'gender' : 'Gender',
            'alamat' : 'Alamat',
            'negara' : 'Negara',
            'kota' : 'Kota',
            'no_hp' : 'HP',
            'univ' : 'Univ',
            'jurusan' : 'Jurusan',
            'ang_kuliah' : '12',
            'ang_LMD' : '12',
            'pekerjaan' : 'pekerjaan',
            'instansi' : 'instansi',
            'aktifitas' : '["aktifitas"]',
            'tahun_aktif' : '["tahun_aktif"]',
            'password' : 'password',
            'latitude' : 1.0,
            'longitude' : 1.0,
            'pertanyaan1' : 'asd',
            'pertanyaan2' : 'asd',
            'jawaban1' : 'asd',
            'jawaban2' : 'asd'
        }
        response = client.post(reverse('api_register'),content_type='application/json',data=json.dumps(payload))
        self.assertTrue(response.data['success'])
    
    def test_api_email(self):
        payload = {
            'email' : 'Email@gmail.com',
        }
        payload2 = {
            'email' : 'Email3@gmail.com'
        }
        response = client.post(reverse('api_email'),content_type='application/json',data=json.dumps(payload))
        response2 = client.post(reverse('api_email'),content_type='application/json',data=json.dumps(payload2))
        self.assertFalse(response.data['data']['available'])
        self.assertTrue(response2.data['data']['available'])
        
    

    
    def test_api_user(self):
        UmToken.objects.create(
            key = 'asd',
            email = 'Email@gmail.com'
        )
        header = {'HTTP_UM' : 'asd'}
        response = client.get(reverse('api_user_get', kwargs= {'id' : '1'}),**header)
        user = User.objects.filter(Q(pk=int(1)))
        img = user.values('profile_image')[0]["profile_image"]
        if img:
            img = "http://" + host + '/media/' + img
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
        self.assertTrue(True)