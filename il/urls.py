from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import api, views


router = DefaultRouter()
router.register(r'agency', api.AgencyViewSet, base_name="agency-api")


urlpatterns = [  # noqa
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^api/', include(router.urls)),
]
