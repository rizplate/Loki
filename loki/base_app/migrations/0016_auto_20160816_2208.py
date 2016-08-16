# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-16 19:08
from __future__ import unicode_literals

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0015_auto_20160623_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('full_image', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='avatar',
            field=image_cropping.fields.ImageCropField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='full_image',
            field=image_cropping.fields.ImageCropField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
