# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0004_auto_20161122_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='character_group_name',
            field=models.CharField(default='Group', max_length=20, verbose_name='Group Name'),
        ),
        migrations.AlterField(
            model_name='splat',
            name='flavor',
            field=models.CharField(choices=[('primary', 'Primary (Nature)'), ('secondary', 'Secondary (Faction)'), ('tertiary', 'Tertiary (Attained)')], max_length=10, null=True),
        ),
    ]
