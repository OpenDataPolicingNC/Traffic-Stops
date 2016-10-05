from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import api, views


router = DefaultRouter()
router.register(r'agency', api.AgencyViewSet, base_name="agency-api")


urlpatterns = [  # noqa
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^agency/$', views.AgencyList.as_view(), name='agency-list'),
    #  FIXME: add actual agency detail view and URL
    url(r'^agency/(?P<pk>\d+)/$', views.AgencyDetail.as_view(),
        name='agency-detail'),
    url(r'^api/', include(router.urls)),
]
