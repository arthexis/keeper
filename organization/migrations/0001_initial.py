# Generated by Django 2.0.4 on 2018-04-11 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chronicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. Must be unique.', max_length=200, unique=True)),
                ('rules_url', models.URLField(blank=True, help_text='URL pointing to the chronicle game and approval rules.', verbose_name='Rules URL')),
                ('short_description', models.TextField(blank=True)),
                ('reference_code', models.SlugField(help_text='Unique short name or acronym.', verbose_name='Reference Code')),
            ],
            options={
                'verbose_name': 'Chronicle',
            },
        ),
        migrations.CreateModel(
            name='GameEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField(blank=True, null=True)),
                ('number', models.PositiveSmallIntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('chronicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_events', to='organization.Chronicle')),
            ],
            options={
                'ordering': ('-event_date',),
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('code', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=8, unique=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('external_id', models.CharField(blank=True, max_length=20, verbose_name='External ID')),
                ('email_address', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('active', 'Active'), ('suspended', 'Suspended')], default='active', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('title', models.CharField(blank=True, choices=[('storyteller', 'Storyteller'), ('coordinator', 'Coordinator')], max_length=20)),
                ('external_id', models.CharField(blank=True, max_length=20, verbose_name='External ID')),
                ('prestige_total', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ('organization__name', 'user__username'),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. Must be unique.', max_length=200, unique=True)),
                ('rules_url', models.URLField(blank=True, help_text='URL pointing to the organization rules document.', verbose_name='Rules URL')),
                ('reference_code', models.SlugField(help_text='Unique short name or acronym.', verbose_name='Reference Code')),
                ('prestige_cutoff', models.DateField(blank=True, null=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='organizations', to='sites.Site')),
            ],
            options={
                'verbose_name': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='Prestige',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('amount', models.PositiveSmallIntegerField()),
                ('notes', models.CharField(blank=True, max_length=400)),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestige', to='organization.Membership')),
            ],
            options={
                'verbose_name': 'Prestige Line',
                'ordering': ('membership',),
            },
        ),
        migrations.CreateModel(
            name='PrestigeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=40)),
                ('prestige_required', models.PositiveSmallIntegerField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestige_levels', to='organization.Organization')),
            ],
            options={
                'verbose_name': 'Prestige Level',
                'ordering': ('prestige_required',),
            },
        ),
        migrations.CreateModel(
            name='PrestigeReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestige_reports', to='organization.Organization')),
            ],
            options={
                'verbose_name': 'Prestige Report',
            },
        ),
        migrations.AddField(
            model_name='prestige',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='organization.PrestigeReport'),
        ),
        migrations.AddField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='membership',
            name='prestige_level',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memberships', to='organization.PrestigeLevel'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitation',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='chronicle',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chronicles', to='organization.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='prestigelevel',
            unique_together={('organization', 'name'), ('organization', 'level')},
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'organization')},
        ),
        migrations.AlterUniqueTogether(
            name='gameevent',
            unique_together={('number', 'chronicle')},
        ),
    ]
