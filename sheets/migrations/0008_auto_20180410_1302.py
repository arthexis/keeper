# Generated by Django 2.0.2 on 2018-04-10 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0007_auto_20180410_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthtracker',
            old_name='health',
            new_name='character',
        ),
    ]
