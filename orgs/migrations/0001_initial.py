# Generated by Django 2.0.2 on 2018-02-19 14:10

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('information', models.TextField(blank=True, help_text='Optional. Basic summary about the event.')),
                ('external_url', models.URLField(blank=True, help_text='Optional. External link containing additional information.', null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-event_date',),
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('is_officer', models.BooleanField(default=False)),
                ('is_owner', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('organization__name',),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(help_text='Required. Must be unique across all Organizations.', max_length=200, unique=True)),
                ('information', models.TextField(blank=True, help_text='Information about your organization. If you set this Organization to be public, everyone will be able to see this information.')),
                ('is_public', models.BooleanField(default=True, help_text='Allow finding the organization and requesting membership.', verbose_name='Open to the Public')),
                ('reference_code', models.SlugField(unique=True, verbose_name='URL Prefix')),
                ('parent_org', models.ForeignKey(blank=True, help_text='Optional. If set, you will inherit settings and staff.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='orgs.Organization', verbose_name='Parent Organization')),
            ],
            options={
                'abstract': False,
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
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestige', to='orgs.Membership')),
            ],
            options={
                'verbose_name': 'Prestige Record',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, parent_link=True, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(blank=True, help_text='Optional. Only shared with Organizations you join.', max_length=20)),
                ('is_verified', models.BooleanField(default=False, editable=False)),
                ('last_visit', models.DateTimeField(blank=True, editable=False, null=True)),
                ('verification_code', models.CharField(blank=True, editable=False, max_length=14, null=True)),
                ('code_sent_on', models.DateTimeField(blank=True, editable=False, null=True)),
                ('org_create_cap', models.SmallIntegerField(default=5, editable=False)),
                ('information', models.TextField(blank=True, help_text='Optional. Personal information shared with others.', null=True)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='prestige',
            name='witness',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='orgs.Organization'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='orgs.Organization'),
        ),
        migrations.CreateModel(
            name='UpcomingEvent',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('orgs.event',),
            managers=[
                ('upcoming', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'organization')},
        ),
    ]
