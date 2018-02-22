# Generated by Django 2.0.2 on 2018-02-22 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. Must be unique.', max_length=200, unique=True)),
                ('information', models.TextField(blank=True)),
                ('reference_code', models.SlugField(help_text='Required. Must be unique.', unique=True, verbose_name='URL Prefix')),
            ],
            options={
                'verbose_name': 'Chapter',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. Must be unique.', max_length=200, unique=True)),
                ('information', models.TextField(blank=True)),
                ('reference_code', models.SlugField(help_text='Required. Must be unique.', unique=True, verbose_name='URL Prefix')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='organization.Chapter')),
            ],
            options={
                'verbose_name': 'Domain',
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
                ('external_id', models.CharField(blank=True, max_length=20)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='organization.Chapter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('chapter__name', 'user__username'),
            },
        ),
        migrations.CreateModel(
            name='Prestige',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('amount', models.IntegerField()),
                ('notes', models.CharField(max_length=2000)),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestige', to='organization.Membership')),
                ('witness', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Prestige Record',
            },
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'chapter')},
        ),
    ]
