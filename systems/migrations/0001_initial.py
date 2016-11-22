# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 05:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import systems.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('is_style', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('dots', systems.fields.DotsField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True)),
                ('dots', systems.fields.DotsField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PowerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('alias', models.CharField(max_length=20)),
                ('integrity_name', models.CharField(max_length=20)),
                ('power_stat_name', models.CharField(max_length=20)),
                ('initial_power_stat', systems.fields.DotsField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
                ('initial_integrity', systems.fields.DotsField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
            ],
        ),
        migrations.AddField(
            model_name='powercategory',
            name='template',
            field=models.ManyToManyField(related_name='powers', to='systems.Template'),
        ),
        migrations.AddField(
            model_name='power',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='powers', to='systems.PowerCategory'),
        ),
        migrations.AddField(
            model_name='merit',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='systems.Template'),
        ),
        migrations.AlterUniqueTogether(
            name='power',
            unique_together=set([('name', 'category', 'dots')]),
        ),
        migrations.AlterUniqueTogether(
            name='merit',
            unique_together=set([('name', 'dots')]),
        ),
    ]
