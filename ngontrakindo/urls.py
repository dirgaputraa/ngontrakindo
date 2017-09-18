"""ngontrakindo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from home.views import index
from django.conf import settings
from django.conf.urls.static import static
from kontrakan.views import *
from profiles.views import *
from search.views import *
urlpatterns = [
	url(r'^$', index, name='home'),
    url(r'^admin/', admin.site.urls),
    # api
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/lokasi/$', LokasiData.as_view(), name='lokasi'),
    url(r'^api/detail-kontrakan/$', DetailKontrakan.as_view(), name='detail_kontrakan'),
    # regist
    url(r'^lengkapi-data/', lengkapi, name='lengkapi'),
    url(r'^lengkapi-data-2/', lengkapi2, name='lengkapi2'),
    # edit profil
    url(r'^edit-profil/profil$', profil_edit, name='profil_edit'),
    url(r'^edit-profil/akun$', akun_edit, name='akun_edit'),
    url(r'^edit-profil/medsos$', medsos_edit, name='medsos_edit'),
    url(r'^edit-profil/$', avatar_edit, name='editprofil'),
    # cari-kontrakan
    url(r'^cari-kontrakan/$', search_view, name='search_view'),
    # administrasi
    url(r'^administrasi/dashboard/(?P<slug>[\w.@+-]+)/$', dashboard_view, name='dashboard_view'),
    url(r'^administrasi/kontrakan/(?P<slug>[\w.@+-]+)/$', kontrakan_view, name='kontrakan_view'),
    url(r'^administrasi/galeri/(?P<slug>[\w.@+-]+)/$', galeri_view, name='galeri_view'),
    url(r'^administrasi/penghuni/(?P<slug>[\w.@+-]+)/$', penghuni_view, name='penghuni_view'),
    url(r'^administrasi/ulasan/(?P<slug>[\w.@+-]+)/$', ulasan_view, name='ulasan_view'),
    url(r'^administrasi/user/(?P<slug>[\w.@+-]+)/$', user_view, name='user_view'),
    url(r'^administrasi/transaksi/(?P<slug>[\w.@+-]+)/$', transaksi_view, name='transaksi_view'),
    url(r'^administrasi/$', admin_view, name='dashboard'),
    # form-kontrakan
    url(r'^daftar/$', DaftarView.as_view(), name='daftar'),
    url(r'^form-kontrakan/1$', KontrakanView.as_view(), name='form_kontrakan'),
    url(r'^form-kontrakan/2$', FasilitasView.as_view(), name='form_fasilitas'),
    url(r'^form-kontrakan/3$', AdministrasiView.as_view(), name='form_administrasi'),
    # user profil
    url(r'^(?P<username>[\w.@+-]+)/$', profil_detail, name='profil'),
    # kontrakan profil
    url(r'^k/(?P<slug>[\w.@+-]+)/$', kontrakan_detailview, name='profilkontrakan'),
    # allauth
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
