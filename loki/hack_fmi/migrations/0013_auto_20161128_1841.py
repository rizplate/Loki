# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-28 16:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0012_seasoncompetitorinfo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seasoncompetitorinfo',
            unique_together=set([('competitor', 'season')]),
        ),
    ]
