# Generated by Django 2.0.2 on 2018-02-19 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0004_power_origin_splat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AttributePrerequisite',
            fields=[
                ('prerequisite_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='systems.Prerequisite')),
                ('attribute', models.CharField(choices=[('strength', 'Strength'), ('dexterity', 'Dexterity'), ('stamina', 'Stamina'), ('intelligence', 'Intelligence'), ('wits', 'Wits'), ('resolve', 'Resolve'), ('presence', 'Presence'), ('manipulation', 'Manipulation'), ('composure', 'Composure')], max_length=20)),
                ('min_value', models.PositiveSmallIntegerField()),
                ('merit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_prerequisites', to='systems.Merit')),
            ],
            bases=('systems.prerequisite',),
        ),
    ]
