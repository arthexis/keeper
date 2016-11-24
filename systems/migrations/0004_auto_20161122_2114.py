# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-23 03:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0003_auto_20161122_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='primary_anchor_name',
            field=models.CharField(default='Virtue', max_length=20, verbose_name='Primary Anchor'),
        ),
        migrations.AddField(
            model_name='template',
            name='secondary_anchor_name',
            field=models.CharField(default='Vice', max_length=20, verbose_name='Secondary Anchor'),
        ),
        migrations.AlterField(
            model_name='template',
            name='integrity_name',
            field=models.CharField(default='Integrity', max_length=20, verbose_name='Integrity'),
        ),
    ]
