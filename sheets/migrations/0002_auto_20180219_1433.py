# Generated by Django 2.0.2 on 2018-02-19 20:33

from django.db import migrations, models
import systems.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='beats',
        ),
        migrations.RemoveField(
            model_name='character',
            name='experiences',
        ),
        migrations.RemoveField(
            model_name='character',
            name='template_beats',
        ),
        migrations.RemoveField(
            model_name='character',
            name='template_experiences',
        ),
        migrations.AddField(
            model_name='character',
            name='alt_names',
            field=models.CharField(blank=True, max_length=500, verbose_name='Other Names'),
        ),
        migrations.AddField(
            model_name='character',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Name or Alias'),
        ),
        migrations.AlterField(
            model_name='character',
            name='size',
            field=systems.fields.DotsField(default=5, editable=False),
        ),
    ]
