from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (
	
	index,
    verifikasi,
    verifuser,
    verifconfirm,
    about,
    aboutsave,

    menyapaPage,
    menyapaList,
    menyapaEdit,
    menyapaEditSave,
    menyapaEditImage,
    menyapaEditImageSave,

	AboutView,

    UserCreateView,
    UserLoginView,
    EmailLoginView,
    GetUserView,
    UpdateUserView,
    UpdateUserImageView,
    
    MenyapaView,
    MenyapaPageView,
    MenyapaDetailView,
    MenyapaLike,
    
    SearchView,
    PersebaranView,
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'), 
    
    url(r'^verifikasi/$', verifikasi, name='verifikasi'),
    url(r'^verifikasi/user/$', verifuser, name='verifuser'),
    url(r'^verifikasi/confirm/$', verifconfirm, name='verifconfirm'),
    
    url(r'^about/$', about, name='about'),
    url(r'^about/save$', aboutsave, name='aboutsave'),
    
    url(r'^menyapa/page/$', menyapaPage, name='menyapaPage'),
    url(r'^menyapa/list/$', menyapaList, name='menyapaList'),
    url(r'^menyapa/edit/(?P<article_id>\d+)/$', menyapaEdit, name='menyapaEdit'),
    url(r'^menyapa/save/$', menyapaEditSave, name='menyapaEditSave'),
    url(r'^menyapa/image/edit/(?P<article_id>\d+)/$', menyapaEditImage, name='menyapaEditImage'),
    url(r'^menyapa/image/save/$', menyapaEditImageSave, name='menyapaEditImageSave'),

    ############################### API ################################

    url(r'^api/about$', AboutView.as_view(), name='api_about'),

    url(r'^api/register$', UserCreateView.as_view(), name='api_register'),
    url(r'^api/login$', UserLoginView.as_view(), name='api_login'),
    url(r'^api/email$', EmailLoginView.as_view(), name='api_email'),
    url(r'^api/user/get/(?P<id>.+)$', GetUserView.as_view(), name='api_user_get'),
    url(r'^api/user/update$', UpdateUserView.as_view(), name='api_user_update'),
    url(r'^api/user/update/image$', UpdateUserImageView.as_view(), name='api_user_update_image'),

    url(r'^api/search$', SearchView.as_view(), name='api_search'),
    url(r'^api/persebaran$', PersebaranView.as_view(), name='api_persebaran'),

    url(r'^api/menyapa$', MenyapaView.as_view(), name='api_menyapa'),
    url(r'^api/menyapa/page/(?P<page>.+)$', MenyapaPageView.as_view(), name='api_menyapa_page'),
    url(r'^api/menyapa/get$', MenyapaDetailView.as_view(), name='api_menyapa_get'),
    url(r'^api/menyapa/like$', MenyapaLike.as_view(), name='api_menyapa_like')

]