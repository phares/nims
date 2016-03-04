from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^review', views.review, name='review'),
    url(r'^status', views.status, name='status'),
]
