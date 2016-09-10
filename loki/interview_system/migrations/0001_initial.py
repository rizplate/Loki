# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-10 18:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_app', '0016_auto_20160816_2208'),
        ('applications', '0004_applicationinfo_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('has_confirmed', models.BooleanField(default=False)),
                ('has_received_email', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('courses_to_interview', models.ManyToManyField(blank=True, null=True, to='applications.ApplicationInfo')),
                ('interviews', models.ManyToManyField(through='interview_system.Interview', to='applications.Application')),
            ],
            options={
                'abstract': False,
            },
            bases=('base_app.baseuser',),
        ),
        migrations.CreateModel(
            name='InterviewerFreeTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview_system.Interviewer')),
            ],
        ),
        migrations.AddField(
            model_name='interview',
            name='interviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview_system.Interviewer'),
        ),
    ]
