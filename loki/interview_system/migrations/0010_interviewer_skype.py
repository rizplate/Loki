# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-30 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview_system', '0009_interview_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewer',
            name='skype',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
