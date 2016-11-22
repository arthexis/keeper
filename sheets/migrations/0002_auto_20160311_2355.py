# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 05:55
from __future__ import unicode_literals

from django.db import migrations
import systems.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='health_levels',
            field=systems.fields.DotsField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='willpower',
            field=systems.fields.DotsField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0),
        ),
    ]
