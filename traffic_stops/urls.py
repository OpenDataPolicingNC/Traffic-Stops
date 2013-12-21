from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView


admin.autodiscover()


urlpatterns = patterns('',  # noqa
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
