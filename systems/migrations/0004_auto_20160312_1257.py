# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0003_splat_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='splatcategory',
            name='alias',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='template',
            name='alias',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='template',
            name='integrity_name',
            field=models.CharField(max_length=20, verbose_name='Integrity'),
        ),
        migrations.AlterField(
            model_name='template',
            name='power_stat_name',
            field=models.CharField(max_length=20, verbose_name='Power Stat'),
        ),
        migrations.AlterField(
            model_name='template',
            name='resource_name',
            field=models.CharField(max_length=20, verbose_name='Resource'),
        ),
    ]
