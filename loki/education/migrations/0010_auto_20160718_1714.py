# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_auto_20160412_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='partner',
            field=models.ManyToManyField(blank=True, to='base_app.Partner'),
        ),
        migrations.AlterField(
            model_name='courseassignment',
            name='favourite_partners',
            field=models.ManyToManyField(blank=True, to='base_app.Partner'),
        ),
    ]
