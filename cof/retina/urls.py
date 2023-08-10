# Copyrights 2020,  Sankara Netralaya & BITS Pilani,
# Contact: sundaresan.raman@pilani.bits-pilani.ac.in

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from . import views
from django.contrib import admin
from django.urls import re_path, path


app_name = 'retina'
urlpatterns = [
    # /retina/
    # re_path(r'^$', views.index, name='index'),
    path('', views.index, name='index'),

    # /retina/last/
    re_path(r'^last/$', views.last, name='last'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
