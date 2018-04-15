from .models import About, User, ArticleClip
from django.db.models import Q
from rest_framework.serializers import (
	CharField,
	EmailField,
	BooleanField,
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField,
	ValidationError,
)

class EmailSerializer(ModelSerializer):
	available = BooleanField(default=True, read_only=True)
	message = CharField(allow_blank=True, read_only=True)
	class Meta:
		model = User
		fields = [
			'email',
			'message',
			'available',
		]

	def validate(self, data):
		email = data['email']
		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			data["available"] = False
			data["message"] = "Email sudah terdaftar"
		else:
			data["available"] = True
			data["message"] = "Email tersedia"

		return data

class GetUserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'nama',
			'email',
			'gender',
			'alamat',
			'kota',
			'kota',
			'no_hp',
			'univ',
			'jurusan',
			'ang_kuliah',
			'ang_LMD',
			'pekerjaan',
			'instansi',
			'aktifitas',
			'tahun_aktif',
			'profile_image',
			'latitude',
			'longitude',
		]

class CreateSeliazier(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'nama',
			'email',
			'gender',
			'alamat',
			'negara',
			'kota',
			'no_hp',
			'univ',
			'jurusan',
			'ang_kuliah',
			'ang_LMD',
			'pekerjaan',
			'instansi',
			'aktifitas',
			'tahun_aktif',
			'password',
			'latitude',
			'longitude',
			'pertanyaan1',
			'pertanyaan2',
			'jawaban1',
			'jawaban2'
		]
		extra_kwargs = {"password":{"write_only": True}}

	def validate(self, data):
		email = data['email']
		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			raise ValidationError("Email sudah terdaftar!")

		return data

class LoginSerializer(ModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	email = EmailField(label='Email Address', required=False, allow_blank=True)
	verified = BooleanField(default=False, read_only=True)
	class Meta:
		model = User
		fields = [
			'email', 
			'password',
			'token',
			'verified',
			'id',
		]
		extra_kwargs = {"password":{"write_only": True}}

	def validate(self, data):
		user_obj = None
		email = data.get("email", None)
		password = data["password"]
		if not email:
			raise ValidationError("Email atau Password salah!!")
		user = User.objects.filter(Q(email=email)).distinct()
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("Email atau Password salah!")

		if user_obj:
			if user_obj.password != password:
				raise ValidationError("Email atau Password salah!")

		data["verified"] = user_obj.verified
		if user_obj.verified:
			data["token"] = "somerandomtoken"
			data["id"] = user_obj.id
		else:
			data["token"] = None

		return data