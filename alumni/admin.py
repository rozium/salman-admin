# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, About

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ['nama', 'email']

class AboutAdmin(admin.ModelAdmin):
	list_display = ['text_alamat', 'text_no_hp', 'text_email']

admin.site.register(User, UserAdmin)
admin.site.register(About, AboutAdmin)