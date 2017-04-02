# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import systems.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('systems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('completed_on', models.DateField(blank=True, null=True, editable=False)),
                ('player_notes', models.TextField(blank=True)),
                ('details', models.TextField(help_text='First 80 characters of the first line will show as a summary.')),
                ('status', models.CharField(max_length=20, default='pending', choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])),
                ('spent_experience', models.SmallIntegerField(verbose_name='Spent Exp', default=0)),
                ('version', models.IntegerField(blank='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aspiration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category', models.CharField(max_length=40, choices=[('information', 'Gather information'), ('resources', 'Gather resources'), ('integrity', 'Develop integrity'), ('aggressive', 'Aggressive action'), ('background', 'Develop background')])),
                ('player_aspiration', models.TextField(blank=True)),
                ('storyteller_response', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assistance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('storyteller_beats', models.SmallIntegerField(verbose_name='Story beats', default=0)),
                ('coordinator_beats', models.SmallIntegerField(verbose_name='Org beats', default=0)),
                ('details', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Character', max_length=40)),
                ('power_stat', systems.fields.DotsField(default=1)),
                ('integrity', systems.fields.DotsField(default=7)),
                ('background', models.TextField(blank=True)),
                ('resource', models.PositiveIntegerField(default=10)),
                ('concept', models.CharField(max_length=200, blank=True)),
                ('faction', models.CharField(max_length=200, blank=True)),
                ('character_group', models.CharField(max_length=100, blank=True)),
                ('strength', systems.fields.DotsField(default=1)),
                ('dexterity', systems.fields.DotsField(default=1)),
                ('stamina', systems.fields.DotsField(default=1)),
                ('intelligence', systems.fields.DotsField(default=1)),
                ('wits', systems.fields.DotsField(default=1)),
                ('resolve', systems.fields.DotsField(default=1)),
                ('presence', systems.fields.DotsField(default=1)),
                ('manipulation', systems.fields.DotsField(default=1)),
                ('composure', systems.fields.DotsField(default=1)),
                ('academics', systems.fields.DotsField(default=0)),
                ('computer', systems.fields.DotsField(default=0)),
                ('crafts', systems.fields.DotsField(default=0)),
                ('investigation', systems.fields.DotsField(default=0)),
                ('medicine', systems.fields.DotsField(default=0)),
                ('occult', systems.fields.DotsField(default=0)),
                ('politics', systems.fields.DotsField(default=0)),
                ('science', systems.fields.DotsField(default=0)),
                ('athletics', systems.fields.DotsField(default=0)),
                ('brawl', systems.fields.DotsField(default=0)),
                ('drive', systems.fields.DotsField(default=0)),
                ('firearms', systems.fields.DotsField(default=0)),
                ('larceny', systems.fields.DotsField(default=0)),
                ('stealth', systems.fields.DotsField(default=0)),
                ('survival', systems.fields.DotsField(default=0)),
                ('weaponry', systems.fields.DotsField(default=0)),
                ('animal_ken', systems.fields.DotsField(default=0)),
                ('empathy', systems.fields.DotsField(default=0)),
                ('expression', systems.fields.DotsField(default=0)),
                ('intimidation', systems.fields.DotsField(default=0)),
                ('persuasion', systems.fields.DotsField(default=0)),
                ('socialize', systems.fields.DotsField(default=0)),
                ('streetwise', systems.fields.DotsField(default=0)),
                ('subterfuge', systems.fields.DotsField(default=0)),
                ('beats', systems.fields.DotsField(default=0)),
                ('experiences', models.PositiveIntegerField(default=0)),
                ('template_beats', systems.fields.DotsField(default=0)),
                ('template_experiences', models.PositiveIntegerField(default=0)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('modified_on', models.DateField(auto_now=True)),
                ('health_levels', models.PositiveIntegerField(default=0)),
                ('willpower', systems.fields.DotsField(default=1)),
                ('primary_anchor', models.CharField(max_length=40, blank=True)),
                ('secondary_anchor', models.CharField(max_length=40, blank=True)),
                ('is_current', models.BooleanField(default=True, editable=False)),
                ('chronicle', models.ForeignKey(blank=True, null=True, related_name='characters', on_delete=django.db.models.deletion.PROTECT, to='orgs.Chronicle')),
                ('player', models.ForeignKey(blank=True, null=True, related_name='characters', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('primary_splat', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.PROTECT, to='systems.SplatOption')),
                ('secondary_splat', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.PROTECT, to='systems.SplatOption')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='systems.Template')),
                ('tertiary_splat', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.PROTECT, to='systems.SplatOption')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterMerit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rating', systems.fields.DotsField(default=1)),
                ('details', models.CharField(max_length=200, blank=True)),
                ('character', models.ForeignKey(related_name='merits', to='sheets.Character')),
                ('merit', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, to='systems.Merit')),
            ],
            options={
                'verbose_name': 'Merit',
            },
        ),
        migrations.CreateModel(
            name='CharacterPower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rating', systems.fields.DotsField(default=1)),
                ('details', models.CharField(max_length=200, blank=True)),
                ('character', models.ForeignKey(related_name='powers', to='sheets.Character')),
                ('power', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, to='systems.Power')),
            ],
            options={
                'verbose_name': 'Power',
            },
        ),
        migrations.CreateModel(
            name='Downtime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sent_on', models.DateField(null=True, editable=False)),
                ('comments', models.TextField(blank=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('character', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, to='sheets.Character')),
                ('event', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, to='orgs.Event')),
            ],
            options={
                'verbose_name_plural': 'Downtime',
            },
        ),
        migrations.CreateModel(
            name='SkillSpeciality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('skill', models.CharField(max_length=20, choices=[('academics', 'Academics'), ('computer', 'Computer'), ('crafts', 'Crafts'), ('investigation', 'Investigation'), ('medicine', 'Medicine'), ('occult', 'Occult'), ('politics', 'Politics'), ('science', 'Science'), ('athletics', 'Athletics'), ('brawl', 'Brawl'), ('drive', 'Drive'), ('firearms', 'Firearms'), ('larceny', 'Larceny'), ('stealth', 'Stealth'), ('survival', 'Survival'), ('weaponry', 'Weaponry'), ('animal_ken', 'Animal Ken'), ('empathy', 'Empathy'), ('expression', 'Expression'), ('intimidation', 'Intimidation'), ('persuasion', 'Persuasion'), ('socialize', 'Socialize'), ('streetwise', 'Streetwise'), ('subterfuge', 'Subterfuge')])),
                ('speciality', models.CharField(max_length=200)),
                ('character', models.ForeignKey(related_name='specialities', to='sheets.Character')),
            ],
            options={
                'verbose_name': 'Skill Speciality',
                'verbose_name_plural': 'Skill Specialities',
            },
        ),
        migrations.AddField(
            model_name='assistance',
            name='character',
            field=models.ForeignKey(related_name='assistance', on_delete=django.db.models.deletion.PROTECT, to='sheets.Character'),
        ),
        migrations.AddField(
            model_name='assistance',
            name='event',
            field=models.ForeignKey(related_name='assistance', on_delete=django.db.models.deletion.PROTECT, to='orgs.Event'),
        ),
        migrations.AddField(
            model_name='aspiration',
            name='downtime',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, to='sheets.Downtime'),
        ),
        migrations.AddField(
            model_name='approvalrequest',
            name='character',
            field=models.ForeignKey(null=True, related_name='approval_requests', to='sheets.Character'),
        ),
        migrations.CreateModel(
            name='PendingApproval',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('sheets.approvalrequest',),
        ),
        migrations.AlterUniqueTogether(
            name='downtime',
            unique_together=set([('character', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='assistance',
            unique_together=set([('character', 'event')]),
        ),
    ]
