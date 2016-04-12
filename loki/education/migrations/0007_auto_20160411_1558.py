# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20160410_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='file',
            field=models.FileField(upload_to='solutions', null=True, blank=True),
        ),
    ]
