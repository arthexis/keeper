# Generated by Django 2.0.2 on 2018-02-20 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='characterpower',
            name='details',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
