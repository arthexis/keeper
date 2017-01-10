# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-10 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0027_auto_20170109_2214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charactermerit',
            old_name='notes',
            new_name='detail',
        ),
        migrations.RenameField(
            model_name='characterpower',
            old_name='notes',
            new_name='detail',
        ),
        migrations.AlterField(
            model_name='character',
            name='version',
            field=models.IntegerField(editable=False, null=True),
        ),
    ]
