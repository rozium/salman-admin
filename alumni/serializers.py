from .models import About, User
from django.db.models import Q
from rest_framework.serializers import (
	CharField,
	EmailField,
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField,
	ValidationError,
)


class AboutSerializer(ModelSerializer):
	class Meta:
		model = About
		fields = ('text_about', 'text_alamat', 'text_no_hp', 'text_email')

class CreateSeliazier(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'nama',
			'email',
			'password',
			# TODO: lengkapin
		]
		extra_kwargs = {"password":{"write_only": True}}

	def validate(self, data):
		email = data['email']
		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			raise ValidationError("Email sudah terdaftar!")

		return data

	def create(self, validated_data):
		print(validated_data)
		nama = validated_data['nama']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(
				nama = nama,
				email = email,
				password = password,
			)
		user_obj.save()
		return validated_data

class LoginSerializer(ModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	email = EmailField(label='Email Address', required=False, allow_blank=True)
	class Meta:
		model = User
		fields = [
			'email', 
			'password',
			'token',
		]
		extra_kwargs = {"password":{"write_only": True}}

	def validate(self, data):
		user_obj = None
		email = data.get("email", None)
		password = data["password"]
		if not email:
			raise ValidationError("Email not found!")
		user = User.objects.filter(Q(email=email)).distinct()
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("Email not found!")

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Wrong Password! please try again.")

		data["token"] = "somerandomtoken"

		return data