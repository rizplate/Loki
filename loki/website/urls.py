from django.conf.urls import url

from .views import index, about, courses, partners

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name="about"),
    url(r'^courses/$', courses, name="courses"),
    url(r'^partners/$', partners, name="partners")
]
