from django.conf.urls import patterns, url

from stops import views

urlpatterns = patterns('',  # noqa
    url(r'^search/', views.search, name='stops-search'),
)
