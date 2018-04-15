from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (
	
	index,
    verifikasi,
    verifuser,
    verifconfirm,
    about,
    menyapaList,
    menyapaEdit,
    RedirectMenyapa,

	AboutView,
    UserCreateView,
    UserLoginView,
    EmailLoginView,
    MenyapaView,

)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'), 
    
    url(r'^verifikasi/$', verifikasi, name='verifikasi'),
    url(r'^verifikasi/user/$', verifuser, name='verifuser'),
    url(r'^verifikasi/confirm/$', verifconfirm, name='verifconfirm'),
    
    url(r'^about/$', about, name='about'),
    
    url(r'^menyapa/list/$', menyapaList, name='menyapaList'),
    url(r'^menyapa/edit/(?P<article_id>\d+)/$', menyapaEdit, name='menyapaEdit'),

    url(r'^api/about$', AboutView.as_view(), name='api_about'),
    url(r'^api/register$', UserCreateView.as_view(), name='api_register'),
    url(r'^api/login$', UserLoginView.as_view(), name='api_login'),
    url(r'^api/email$', EmailLoginView.as_view(), name='api_email'),
    url(r'^api/menyapa/(?P<id>.+)$', MenyapaView.as_view(), name='api_menyapa'),
    url(r'^api/menyapa$', RedirectMenyapa, name='api_menyapa'),
]