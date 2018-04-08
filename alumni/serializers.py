from rest_framework import serializers
from .models import About, User

class AboutSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = About
		fields = ('text_about', 'text_alamat', 'text_no_hp', 'text_email')

class LoginSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'password')