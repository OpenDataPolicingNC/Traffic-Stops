from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import HomeView, About, UpdateSession


admin.autodiscover()


urlpatterns = [  # noqa
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^nc/', include('nc.urls', namespace='nc')),
    url(r'^md/', include('md.urls', namespace='md')),
    url(r'^about$', About.as_view(), name='about'),
    url(r'^update-session/', UpdateSession.as_view(), name='update_session'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
