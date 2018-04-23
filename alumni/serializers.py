import random, string
from .models import About, User, ArticleClip, UmToken
from django.db.models import Q
from rest_framework.serializers import (
	CharField,
	EmailField,
	BooleanField,
	ReadOnlyField,
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
			randomToken = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
			data["token"] = randomToken
			UmToken.objects.create(key=randomToken, email=email)
			data["id"] = user_obj.id
		else:
			data["token"] = None

		return data

class UpdatePhotoSerializer(ModelSerializer):
	id = CharField(label='Id', required=False, allow_blank=True)
	class Meta:
		model = User
		fields = ["id", "profile_image"]

		def validate(self, data):

			id_user = data.get("id", None)
			profile_image = data["profile_image"]
			if not id_user or not profile_image:
				raise ValidationError("Terjadi Kesalahan")
			user = User.objects.filter(Q(pk=id_user))
			if user.exists():
				print "haha"
			else:
				raise ValidationError("User tidak ditemuan.")

			return data

class UpdateSerializer(ModelSerializer):
	id = CharField(label='Id', required=False, allow_blank=True)
	class Meta:
		model = User
		fields = [
			'id',
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
			'latitude',
			'longitude',
		]

	def validate(self, data):
		user_obj = None

		id_user = data.get("id", None)

		nama = data.get("nama", None)
		email = data.get("email", None)
		gender = data.get("gender", None)
		alamat = data.get("alamat", None)
		negara = data.get("negara", None)
		kota = data.get("kota", None)
		no_hp = data.get("no_hp", None)
		univ = data.get("univ", None)
		jurusan = data.get("jurusan", None)
		ang_kuliah = data.get("ang_kuliah", None)
		ang_LMD = data.get("ang_LMD", None)
		pekerjaan = data.get("pekerjaan", None)
		instansi = data.get("instansi", None)
		aktifitas = data.get("aktifitas", None)
		tahun_aktif = data.get("tahun_aktif", None)
		latitude = data.get("latitude", None)
		longitude = data.get("longitude", None)

		if not id_user or not nama or not email or not gender or not alamat or not negara or not kota or not no_hp or not univ or not jurusan or not ang_kuliah or not ang_LMD or not pekerjaan or not instansi or not aktifitas or not tahun_aktif or not latitude or not longitude:
			raise ValidationError("Terjadi kesalahan.")
		user = User.objects.filter(Q(pk=id_user))
		if user.exists():
			user.update(
					nama = nama,
					email = email,
					gender = gender,
					alamat = alamat,
					kota = kota,
					negara = negara,
					no_hp = no_hp,
					univ = univ,
					jurusan = jurusan,
					ang_kuliah = ang_kuliah,
					ang_LMD = ang_LMD,
					pekerjaan = pekerjaan,
					instansi = instansi,
					aktifitas = aktifitas,
					tahun_aktif = tahun_aktif,
					latitude = latitude,
					longitude = longitude,
				)
		else:
			raise ValidationError("User tidak ditemuan.")

		return data