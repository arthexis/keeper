# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnchorCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('is_required', models.BooleanField(default=False)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Anchor Category',
                'verbose_name_plural': 'Anchor Categories',
            },
        ),
        migrations.CreateModel(
            name='Merit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reference_book', models.CharField(max_length=100, blank=True)),
                ('reference_page', models.PositiveIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=40)),
                ('category', models.CharField(max_length=20, null=True, choices=[('mental', 'Mental'), ('physical', 'Physical'), ('social', 'Social'), ('supernatural', 'Supernatural'), ('style', 'Style')])),
            ],
            options={
                'ordering': ('template', 'category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reference_book', models.CharField(max_length=100, blank=True)),
                ('reference_page', models.PositiveIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ('category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='PowerCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Power Category',
                'verbose_name_plural': 'Power Categories',
            },
        ),
        migrations.CreateModel(
            name='Splat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('flavor', models.CharField(max_length=10, null=True, choices=[('primary', 'Primary (Nature)'), ('secondary', 'Secondary (Faction)'), ('tertiary', 'Tertiary (Attained)')])),
            ],
            options={
                'ordering': ('template', 'flavor'),
            },
        ),
        migrations.CreateModel(
            name='SplatOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reference_book', models.CharField(max_length=100, blank=True)),
                ('reference_page', models.PositiveIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=40)),
                ('category', models.ForeignKey(related_name='splats', to='systems.Splat')),
            ],
            options={
                'ordering': ('category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('alias', models.CharField(max_length=20, blank=True)),
                ('integrity_name', models.CharField(verbose_name='Integrity', max_length=20, default='Integrity')),
                ('power_stat_name', models.CharField(verbose_name='Power Stat', max_length=20)),
                ('resource_name', models.CharField(verbose_name='Resource', max_length=20)),
                ('primary_anchor_name', models.CharField(verbose_name='Primary Anchor', max_length=20, default='Virtue')),
                ('secondary_anchor_name', models.CharField(verbose_name='Secondary Anchor', max_length=20, default='Vice')),
                ('character_group_name', models.CharField(verbose_name='Group Name', max_length=20, default='Group')),
            ],
        ),
        migrations.AddField(
            model_name='splat',
            name='template',
            field=models.ForeignKey(related_name='splat_categories', to='systems.Template'),
        ),
        migrations.AddField(
            model_name='powercategory',
            name='template',
            field=models.ForeignKey(null=True, related_name='power_categories', on_delete=django.db.models.deletion.PROTECT, to='systems.Template'),
        ),
        migrations.AddField(
            model_name='power',
            name='category',
            field=models.ForeignKey(related_name='powers', on_delete=django.db.models.deletion.PROTECT, to='systems.PowerCategory'),
        ),
        migrations.AddField(
            model_name='merit',
            name='template',
            field=models.ForeignKey(blank=True, null=True, to='systems.Template'),
        ),
        migrations.AddField(
            model_name='anchorcategory',
            name='template',
            field=models.ForeignKey(related_name='anchor_categories', to='systems.Template'),
        ),
        migrations.AlterUniqueTogether(
            name='power',
            unique_together=set([('name', 'category')]),
        ),
    ]
