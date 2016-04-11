from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^account/$', views.account, name='account'),

]
