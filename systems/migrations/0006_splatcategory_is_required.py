# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-22 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0005_auto_20160312_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='splatcategory',
            name='is_required',
            field=models.BooleanField(default=False),
        ),
    ]
