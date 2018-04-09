from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (
	
	index,
	home,
	verifikasi,
	about,
	menyapaList,
	menyapaEdit,

	AboutViewSet,
    UserCreateView,
    UserLoginView,

)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'), 
    url(r'^home/$', home, name='home'), 
    url(r'^verifikasi/$', verifikasi, name='verifikasi'),
    url(r'^about/$', about, name='about'),
    url(r'^menyapa/list/$', menyapaList, name='menyapaList'),
    url(r'^menyapa/edit/(?P<article_id>\d+)/$', menyapaEdit, name='menyapaEdit'),
    url(r'^api/register$', UserCreateView.as_view(), name='api_register'),
]