# Generated by Django 2.0.2 on 2018-02-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0003_auto_20180227_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='alt_names',
        ),
        migrations.AlterField(
            model_name='character',
            name='player_notes',
            field=models.TextField(blank=True, help_text='Visible to player.'),
        ),
        migrations.AlterField(
            model_name='character',
            name='storyteller_notes',
            field=models.TextField(blank=True, help_text='Hidden from player.'),
        ),
    ]
