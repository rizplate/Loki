# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 11:59
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_remove_coursedescription_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='list_courses_text',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Това е малък текст за /courses страницата', null=True),
        ),
    ]