from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload$', views.upload, name='upload'),
    url(r'^choose$', views.choose, name='choose'),
    url(r'^compute$', views.compute, name='compute'),
]
