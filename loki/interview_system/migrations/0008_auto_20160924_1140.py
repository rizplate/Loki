# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-24 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview_system', '0007_auto_20160923_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interview',
            name='code_design_rating',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0, help_text='Оценка върху уменията на кандидата да "съставя програми", да разбива нещата на парчета + базово OOP'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='code_skills_rating',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0, help_text='Оценка върху уменията на кандидата да пише код и върху знанията му за базови алгоритми'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='fit_attitude_rating',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0, help_text='Оценка на интервюиращия в зависимост от усета му за човека (подходящ ли е за курса)'),
        ),
    ]
