from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^status/$', views.status, name='status'),
<<<<<<< HEAD
    url(r'^report/$', views.download_report, name='report'),
=======
    url(r'^create/$', views.create, name='create'),
    url(r'^account/$', views.account, name='account'),
    url(r'^lipisha/$', views.lipisha_, name='lipisha'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test/(?P<id>\d+)/$', views.test_detail, name='test_detail'),
    url(r'^(?P<id>\d+)/edit/$', views.update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name='delete'),
>>>>>>> 1c397ea447c8373aebf3f07fe88b5cf2e784e640

]
