# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0010_auto_20170107_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillspeciality',
            name='skill',
            field=models.CharField(choices=[('academics', 'Academics'), ('computer', 'Computer'), ('crafts', 'Crafts'), ('investigation', 'Investigation'), ('medicine', 'Medicine'), ('occult', 'Occult'), ('politics', 'Politics'), ('science', 'Science'), ('athletics', 'Athletics'), ('brawl', 'Brawl'), ('drive', 'Drive'), ('firearms', 'Firearms'), ('larceny', 'Larceny'), ('stealth', 'Stealth'), ('survival', 'Survival'), ('weaponry', 'Weaponry'), ('animal_ken', 'Animal Ken'), ('empathy', 'Empathy'), ('expression', 'Expression'), ('intimidation', 'Intimidation'), ('persuasion', 'Persuasion'), ('socialize', 'Socialize'), ('streetwise', 'Streetwise'), ('subterfuge', 'Subterfuge')], max_length=20),
        ),
    ]
