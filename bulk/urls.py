from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^index/$', views.index, name='index'),
    url(r'^review/$', views.review, name='review'),
    url(r'^status/$', views.status, name='status'),
    url(r'^create/$', views.create, name='create'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test/(?P<id>\d+)/$', views.test_detail, name='test_detail'),
    url(r'^(?P<id>\d+)/edit/$', views.update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name='delete'),

]
