from django.db import models

from hack_fmi.models import BaseUser


class HR(BaseUser):
    phone = models.CharField(null=True, blank=True, max_length='20')
    company = models.ForeignKey('base_app.Partner')