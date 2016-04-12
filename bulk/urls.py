from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^status/$', views.status, name='status'),
    url(r'^report/$', views.download_report, name='report'),

]
