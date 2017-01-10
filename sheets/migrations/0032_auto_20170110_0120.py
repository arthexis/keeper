# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-10 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0031_auto_20170110_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalrequest',
            name='spent_experience',
            field=models.SmallIntegerField(default=0, verbose_name='Spent Exp'),
        ),
        migrations.AlterField(
            model_name='character',
            name='spent_experience',
            field=models.SmallIntegerField(default=0, editable=False, verbose_name='Spent Exp'),
        ),
    ]
