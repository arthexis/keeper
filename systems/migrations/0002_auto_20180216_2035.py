# Generated by Django 2.0.2 on 2018-02-17 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splatcategory',
            name='flavor',
            field=models.CharField(choices=[('1', 'Primary: Nature'), ('2', 'Secondary: Faction'), ('3', 'Tertiary: Attained')], max_length=1, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='splatcategory',
            unique_together=set(),
        ),
    ]