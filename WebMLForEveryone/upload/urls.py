from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload$', views.upload, name='upload'),
    url(r'^choose/(?P<id>[0-9]+)$', views.choose, name='choose'),
    url(r'^compute/(?P<id>[0-9]+)/(?P<column>.+)/(?P<model>.+)$', views.compute, name='compute'),
    url(r'^ajax/choose/', views.ajax_choose_model, name='ajax_choose_model'),
    url(r'^ajax/compute/', views.ajax_predict, name='ajax_predict'),
]
