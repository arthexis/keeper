# Generated by Django 2.0.2 on 2018-03-26 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180326_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestigelevel',
            name='level',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='prestigelevel',
            unique_together={('organization', 'level'), ('organization', 'name')},
        ),
    ]
