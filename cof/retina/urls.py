# Copyrights 2020,  Sankara Netralaya & BITS Pilani,
# Contact: sundaresan.raman@pilani.bits-pilani.ac.in

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from . import views
from django.contrib import admin
from django.urls import re_path


app_name = 'retina'


urlpatterns = [
    # /retina/
    re_path(r'^$', views.index, name='index'),

    # /retina/cf/
    re_path(r'^cf/', views.cf, name='cf'),

    # /retina/ma/
    re_path(r'^ma/$', views.ma, name='ma'),

    # /retina/rh/
    re_path(r'^rh/$', views.rh, name='rh'),

    # /retina/he/
    re_path(r'^he/$', views.he, name='he'),

    # /retina/cws/
    re_path(r'^cws/$', views.cws, name='cws'),

    # /retina/nve/
    re_path(r'^nve/$', views.nve, name='nve'),

    # /retina/nvd/
    re_path(r'^nvd/$', views.nvd, name='nvd'),

    # /retina/sh/
    re_path(r'^sh/$', views.sh, name='sh'),

    # /retina/vh/
    re_path(r'^vh/$', views.vh, name='vh'),

    # /retina/last/
    re_path(r'^last/$', views.last, name='last'),

    # /retina/<patient_id>/
    re_path(r'^(?P<patient_id>[0-9]+)/$', views.detail, name='detail'),

    # /retina/<patient_id>/process/
    re_path(r'^(?P<patient_id>[0-9]+)/process/$', views.process, name='process'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
