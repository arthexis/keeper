# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('systems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chronicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Chronicle Name', max_length=40)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('mood', models.CharField(max_length=200, blank=True)),
                ('theme', models.CharField(max_length=200, blank=True)),
                ('information', models.TextField(blank=True)),
                ('coordinating_group', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='auth.Group')),
                ('default_template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='systems.Template')),
                ('domain_coordinator', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('domain_storyteller', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('storytelling_group', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='auth.Group')),
                ('venue_coordinator', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('venue_storyteller', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Event Name', max_length=40)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('information', models.TextField(blank=True)),
                ('planning_document', models.URLField(blank=True)),
                ('seq', models.SmallIntegerField(null=True, editable=False)),
                ('chronicle', models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.PROTECT, to='orgs.Chronicle')),
            ],
            options={
                'ordering': ('-event_date',),
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.CharField(max_length=20, default='provisional', choices=[('hold', 'On Hold'), ('provisional', 'Provisional'), ('active', 'Active'), ('expired', 'Expired'), ('cancelled', 'Cancelled')])),
                ('joined_on', models.DateField(verbose_name='Joined', blank=True, null=True)),
                ('starts_on', models.DateField(verbose_name='Starts', blank=True, null=True)),
                ('ends_on', models.DateField(verbose_name='Ends', blank=True, null=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('user', models.OneToOneField(related_name='membership', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prestige',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('prestige_beats', models.SmallIntegerField(default=0)),
                ('details', models.TextField(blank=True)),
                ('awarded_on', models.DateField(auto_now_add=True)),
                ('membership', models.ForeignKey(related_name='prestige', on_delete=django.db.models.deletion.PROTECT, to='orgs.Membership')),
            ],
        ),
    ]
