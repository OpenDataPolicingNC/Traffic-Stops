from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from nc.views import home, UpdateSession


admin.autodiscover()


urlpatterns = patterns('',  # noqa
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^', include('nc.urls')),
    url(r'^update-session/', UpdateSession.as_view(), name='update_session'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
