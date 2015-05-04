from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.URLField(blank=True)
    jobs_link = models.URLField(blank=True)
