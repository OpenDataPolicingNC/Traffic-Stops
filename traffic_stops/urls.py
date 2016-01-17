from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from nc import views


admin.autodiscover()


urlpatterns = [  # noqa
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^', include('nc.urls')),
    url(r'^about$', views.About.as_view(), name='about'),
    url(r'^update-session/', views.UpdateSession.as_view(), name='update_session'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
