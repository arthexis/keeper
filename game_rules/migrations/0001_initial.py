# Generated by Django 2.0.2 on 2018-02-24 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnchorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('is_required', models.BooleanField(default=False)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Anchor Category',
                'verbose_name_plural': 'Anchor Categories',
            },
        ),
        migrations.CreateModel(
            name='CharacterTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('game_line', models.CharField(choices=[('gmc', 'God Machine Chronicles'), ('vtr', 'Vampire the Requiem'), ('ctl', 'Changeling the Lost'), ('mtaw', 'Mage the Awakening'), ('wtf', 'Werewolf the Forsaken'), ('gts', 'Geist the Sin-Eaters')], max_length=20)),
                ('integrity_name', models.CharField(blank=True, default='Integrity', max_length=20, verbose_name='Integrity')),
                ('power_stat_name', models.CharField(blank=True, max_length=20, verbose_name='Power Stat')),
                ('resource_name', models.CharField(blank=True, max_length=20, verbose_name='Resource')),
                ('primary_anchor_name', models.CharField(blank=True, default='Virtue', max_length=20, verbose_name='Primary Anchor')),
                ('secondary_anchor_name', models.CharField(blank=True, default='Vice', max_length=20, verbose_name='Secondary Anchor')),
                ('character_group_name', models.CharField(blank=True, default='Group', max_length=20, verbose_name='Group Name')),
                ('experiences_prefix', models.CharField(blank=True, max_length=20, null=True, verbose_name='Experiences Prefix')),
                ('reference_code', models.SlugField(unique=True, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Character Template',
                'ordering': ('name', 'game_line'),
            },
        ),
        migrations.CreateModel(
            name='Merit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('reference_code', models.SlugField(unique=True, verbose_name='Code')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ('power_category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='PowerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('character_template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='power_categories', to='game_rules.CharacterTemplate')),
            ],
            options={
                'verbose_name': 'Power Category',
                'verbose_name_plural': 'Power Categories',
            },
        ),
        migrations.CreateModel(
            name='ReferenceBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('reference_code', models.SlugField(max_length=10, unique=True, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Reference Book',
            },
        ),
        migrations.CreateModel(
            name='Splat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ('splat_category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='SplatCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('flavor', models.CharField(choices=[('primary', 'Primary Kind'), ('primary_sub', 'Secondary Kind'), ('secondary', 'Major Faction'), ('secondary_sub', 'Minor Faction'), ('tertiary', 'Tertiary Kind')], max_length=20)),
                ('is_required', models.BooleanField(default=False)),
                ('character_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='splat_categories', to='game_rules.CharacterTemplate')),
            ],
            options={
                'verbose_name': 'Splat Category',
                'verbose_name_plural': 'Splat Categories',
                'ordering': ('character_template', 'flavor'),
            },
        ),
        migrations.AddField(
            model_name='splat',
            name='splat_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='splats', to='game_rules.SplatCategory'),
        ),
        migrations.AddField(
            model_name='power',
            name='power_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powers', to='game_rules.PowerCategory'),
        ),
        migrations.AddField(
            model_name='anchorcategory',
            name='character_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anchor_categories', to='game_rules.CharacterTemplate'),
        ),
        migrations.AlterUniqueTogether(
            name='splatcategory',
            unique_together={('character_template', 'flavor')},
        ),
        migrations.AlterUniqueTogether(
            name='splat',
            unique_together={('name', 'splat_category')},
        ),
        migrations.AlterUniqueTogether(
            name='power',
            unique_together={('name', 'power_category')},
        ),
    ]
