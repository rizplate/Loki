from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hackfmi/', include('loki.hack_fmi.urls', namespace='hack_fmi')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^education/', include('loki.education.urls', namespace='education')),
    url(r'^base/', include('loki.base_app.urls', namespace='base_app')),
    url(r'^apply/', include('loki.applications.urls', namespace='applications')),
    url(r'^interview/', include('loki.interview_system.urls', namespace='interview_system')),
    url(r'^', include('loki.website.urls', namespace='website')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
