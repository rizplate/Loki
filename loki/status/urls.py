from django.conf.urls import url
from status.views import check_raspberry

urlpatterns = [
    url(r'^api/check-raspberry/$', check_raspberry, name='check_raspberry'),
]