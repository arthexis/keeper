# Generated by Django 2.0.2 on 2018-02-20 15:14

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='approvalrequest',
            managers=[
                ('pending', django.db.models.manager.Manager()),
            ],
        ),
    ]