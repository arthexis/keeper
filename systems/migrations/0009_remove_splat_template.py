# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-22 06:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0008_splat_is_playable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splat',
            name='template',
        ),
    ]
