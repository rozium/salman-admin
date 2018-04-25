# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,ArticleClip,About

client = Client()
# Create your tests here.
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
