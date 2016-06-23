from django.conf.urls import url

from md import views

urlpatterns = [
    url(r'^$', views.home, name='md-home'),
]
