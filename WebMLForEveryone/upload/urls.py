from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^index/', TemplateView.as_view(template_name='index.html')),
    url(r'^contact/', TemplateView.as_view(template_name='contact.html')),
    url(r'^about/', TemplateView.as_view(template_name='about.html')),

    url(r'^upload$', views.upload, name='upload'),
    url(r'^choose/(?P<id>[0-9]+)/$', views.choose, name='choose'),
    url(r'^compute/(?P<model_builder>[0-9]+)/$', views.compute, name='compute'),

    url(r'^ajax/choose_model/', views.ajax_choose_model, name='ajax_choose_model'),
    url(r'^ajax/train_model/', views.ajax_train_model, name='ajax_train_model'),
    url(r'^ajax/predict/', views.ajax_predict, name='ajax_predict'),
    url(r'^ajax/upload_file/', views.ajax_upload_file, name='ajax_upload_file'),
    url(r'^ajax/upload_predict_save/', views.ajax_upload_predict_save, name='ajax_upload_predict_save'),
    url(r'^ajax/save_to_excel/', views.ajax_save_to_excel, name='ajax_save_to_excel'),
]
