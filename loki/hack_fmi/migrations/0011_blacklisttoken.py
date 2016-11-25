# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-23 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0010_competitor_other_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
