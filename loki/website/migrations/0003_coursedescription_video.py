# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_successstoryperson_show_picture_on_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='video',
            field=models.URLField(blank=True),
        ),
    ]
