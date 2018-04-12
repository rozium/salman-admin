from .models import About, User
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
			'gender',
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
		]
		extra_kwargs = {"password":{"write_only": True}}

	def validate(self, data):
		email = data['email']
		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			raise ValidationError("Email sudah terdaftar!")

		return data

	def create(self, validated_data):
		nama = validated_data['nama']
		email = validated_data['email']
		gender = validated_data['gender']
		negara = validated_data['negara']
		kota = validated_data['kota']
		no_hp = validated_data['no_hp']
		univ = validated_data['univ']
		jurusan = validated_data['jurusan']
		ang_kuliah = validated_data['ang_kuliah']
		ang_LMD = validated_data['ang_LMD']
		pekerjaan = validated_data['pekerjaan']
		instansi = validated_data['instansi']
		aktifitas = validated_data['aktifitas']
		tahun_aktif = validated_data['tahun_aktif']
		password = validated_data['password']
		user_obj = User(
				nama = nama,
				email = email,
				gender = gender,
				negara = negara,
				kota = kota,
				no_hp = no_hp,
				univ = univ,
				jurusan = jurusan,
				ang_kuliah = ang_kuliah,
				ang_LMD = ang_LMD,
				pekerjaan = pekerjaan,
				instansi = instansi,
				aktifitas = aktifitas,
				tahun_aktif = tahun_aktif,
				password = password,
			)
		user_obj.save()
		return validated_data

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
		else:
			data["token"] = None

		return data