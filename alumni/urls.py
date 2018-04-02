from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'), 
    url(r'^home/$', views.home, name='home'), 
    url(r'^verifikasi/$', views.verifikasi, name='verifikasi'),
    url(r'^menyapa/edit/$', views.menyapaEdit, name='menyapaEdit'),
]
