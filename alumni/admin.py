# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, About, ArticleClip, UmToken

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ['nama', 'email']

class AboutAdmin(admin.ModelAdmin):
	list_display = ['text_alamat', 'text_no_hp', 'text_email']

class ArticleClipAdmin(admin.ModelAdmin):
	list_display = ['judul', 'deskripsi', 'updated_at', 'published',]

class UmTokenAdmin(admin.ModelAdmin):
	list_display = ['key', 'email']

admin.site.register(User, UserAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(UmToken, UmTokenAdmin)
admin.site.register(ArticleClip, ArticleClipAdmin)