# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import loki.education.validators


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_auto_20160715_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mac',
            field=models.CharField(max_length=17, null=True, validators=[loki.education.validators.validate_mac]),
        ),
    ]