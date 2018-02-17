# Generated by Django 2.0.2 on 2018-02-17 02:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import systems.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('systems', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Character Name')),
                ('power_stat', systems.fields.DotsField(default=1)),
                ('integrity', systems.fields.DotsField(default=7)),
                ('background', models.TextField(blank=True)),
                ('resource', models.PositiveIntegerField(blank=True, default=10, null=True)),
                ('resource_max', models.PositiveIntegerField(blank=True, default=10, null=True)),
                ('concept', models.CharField(blank=True, max_length=200)),
                ('faction', models.CharField(blank=True, max_length=200)),
                ('character_group', models.CharField(blank=True, max_length=100)),
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
                ('beats', models.PositiveIntegerField(default=0)),
                ('experiences', models.PositiveIntegerField(default=0)),
                ('template_beats', systems.fields.DotsField(default=0)),
                ('template_experiences', models.PositiveIntegerField(default=0)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('modified_on', models.DateField(auto_now=True)),
                ('size', systems.fields.DotsField(default=5)),
                ('health_levels', models.PositiveIntegerField(default=0)),
                ('damage_track', models.CharField(blank=True, max_length=100, null=True)),
                ('willpower', models.PositiveIntegerField(blank=True, null=True)),
                ('willpower_max', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('perm_willpower_spent', models.PositiveIntegerField(blank=True, null=True)),
                ('primary_anchor', models.CharField(blank=True, max_length=40)),
                ('secondary_anchor', models.CharField(blank=True, max_length=40)),
                ('version', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
                ('primary_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='systems.Splat')),
                ('secondary_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='systems.Splat')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='systems.CharacterTemplate')),
                ('tertiary_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='systems.Splat')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='characters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterMerit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', systems.fields.DotsField(default=1)),
                ('details', models.CharField(blank=True, max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merits', to='sheets.Character')),
                ('merit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='systems.Merit')),
            ],
            options={
                'verbose_name': 'Merit',
            },
        ),
        migrations.CreateModel(
            name='CharacterPower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', systems.fields.DotsField(default=1)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powers', to='sheets.Character')),
                ('power', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='systems.Power')),
            ],
            options={
                'verbose_name': 'Power',
            },
        ),
        migrations.CreateModel(
            name='SkillSpeciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(choices=[('academics', 'Academics'), ('computer', 'Computer'), ('crafts', 'Crafts'), ('investigation', 'Investigation'), ('medicine', 'Medicine'), ('occult', 'Occult'), ('politics', 'Politics'), ('science', 'Science'), ('athletics', 'Athletics'), ('brawl', 'Brawl'), ('drive', 'Drive'), ('firearms', 'Firearms'), ('larceny', 'Larceny'), ('stealth', 'Stealth'), ('survival', 'Survival'), ('weaponry', 'Weaponry'), ('animal_ken', 'Animal Ken'), ('empathy', 'Empathy'), ('expression', 'Expression'), ('intimidation', 'Intimidation'), ('persuasion', 'Persuasion'), ('socialize', 'Socialize'), ('streetwise', 'Streetwise'), ('subterfuge', 'Subterfuge')], max_length=20)),
                ('speciality', models.CharField(max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialities', to='sheets.Character')),
            ],
            options={
                'verbose_name': 'Skill Speciality',
                'verbose_name_plural': 'Skill Specialities',
            },
        ),
    ]
