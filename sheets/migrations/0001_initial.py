# Generated by Django 2.0.2 on 2018-03-26 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import game_rules.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('game_rules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advancement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, editable=False, null=True)),
                ('experience', models.PositiveSmallIntegerField(default=0)),
                ('beats', models.PositiveSmallIntegerField(default=0)),
                ('notes', models.CharField(blank=True, max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApprovalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('pending', 'Pending'), ('complete', 'Complete')], default='pending', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('uuid', models.UUIDField(db_index=True, editable=False, null=True)),
                ('description', models.TextField(verbose_name='Request Information')),
                ('experience_cost', models.PositiveSmallIntegerField(default=0)),
                ('attachment', models.BinaryField(blank=True)),
                ('attachment_content_type', models.CharField(blank=True, max_length=100)),
                ('attachment_filename', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'verbose_name': 'Approval Request',
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('in_progress', 'In Progress'), ('approved', 'Approved'), ('archived', 'Archived')], default='in_progress', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('name', models.CharField(db_index=True, max_length=40, verbose_name='Name or Alias')),
                ('power_stat', game_rules.fields.DotsField(default=1)),
                ('integrity', game_rules.fields.DotsField(default=7)),
                ('storyteller_notes', models.TextField(blank=True, help_text='Hidden from player.')),
                ('player_notes', models.TextField(blank=True, help_text='Shown in player sheet.')),
                ('resource_start', models.PositiveIntegerField(blank=True, default=10, null=True)),
                ('resource_max', models.PositiveIntegerField(blank=True, default=10, null=True)),
                ('concept', models.CharField(blank=True, max_length=200)),
                ('faction', models.CharField(blank=True, max_length=200)),
                ('character_group', models.CharField(blank=True, max_length=100)),
                ('strength', game_rules.fields.DotsField(default=1)),
                ('dexterity', game_rules.fields.DotsField(default=1)),
                ('stamina', game_rules.fields.DotsField(default=1)),
                ('intelligence', game_rules.fields.DotsField(default=1)),
                ('wits', game_rules.fields.DotsField(default=1)),
                ('resolve', game_rules.fields.DotsField(default=1)),
                ('presence', game_rules.fields.DotsField(default=1)),
                ('manipulation', game_rules.fields.DotsField(default=1)),
                ('composure', game_rules.fields.DotsField(default=1)),
                ('academics', game_rules.fields.DotsField(default=0)),
                ('computer', game_rules.fields.DotsField(default=0)),
                ('crafts', game_rules.fields.DotsField(default=0)),
                ('investigation', game_rules.fields.DotsField(default=0)),
                ('medicine', game_rules.fields.DotsField(default=0)),
                ('occult', game_rules.fields.DotsField(default=0)),
                ('politics', game_rules.fields.DotsField(default=0)),
                ('science', game_rules.fields.DotsField(default=0)),
                ('athletics', game_rules.fields.DotsField(default=0)),
                ('brawl', game_rules.fields.DotsField(default=0)),
                ('drive', game_rules.fields.DotsField(default=0)),
                ('firearms', game_rules.fields.DotsField(default=0)),
                ('larceny', game_rules.fields.DotsField(default=0)),
                ('stealth', game_rules.fields.DotsField(default=0)),
                ('survival', game_rules.fields.DotsField(default=0)),
                ('weaponry', game_rules.fields.DotsField(default=0)),
                ('animal_ken', game_rules.fields.DotsField(default=0)),
                ('empathy', game_rules.fields.DotsField(default=0)),
                ('expression', game_rules.fields.DotsField(default=0)),
                ('intimidation', game_rules.fields.DotsField(default=0)),
                ('persuasion', game_rules.fields.DotsField(default=0)),
                ('socialize', game_rules.fields.DotsField(default=0)),
                ('streetwise', game_rules.fields.DotsField(default=0)),
                ('subterfuge', game_rules.fields.DotsField(default=0)),
                ('size', models.PositiveSmallIntegerField(default=5)),
                ('speed', models.PositiveSmallIntegerField(default=0)),
                ('initiative', models.PositiveSmallIntegerField(default=0)),
                ('bashing_damage', models.PositiveIntegerField(default=0)),
                ('lethal_damage', models.PositiveIntegerField(default=0)),
                ('aggravated_damage', models.PositiveIntegerField(default=0)),
                ('willpower', game_rules.fields.DotsField(default=0)),
                ('health', game_rules.fields.DotsField(default=0)),
                ('primary_anchor', models.CharField(blank=True, max_length=40)),
                ('secondary_anchor', models.CharField(blank=True, max_length=40)),
                ('version', models.PositiveIntegerField(default=0)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('chronicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', to='organization.Chronicle')),
                ('primary_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Splat')),
                ('primary_sub_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Splat')),
                ('secondary_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Splat')),
                ('secondary_sub_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Splat')),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game_rules.CharacterTemplate')),
                ('tertiary_splat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Splat')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterAnchor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anchors', to='sheets.Character')),
                ('template_anchor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.TemplateAnchor')),
            ],
            options={
                'verbose_name': 'Anchor',
            },
        ),
        migrations.CreateModel(
            name='CharacterMerit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', game_rules.fields.DotsField(default=1)),
                ('details', models.CharField(blank=True, max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merits', to='sheets.Character')),
                ('merit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Merit')),
            ],
            options={
                'verbose_name': 'Merit',
            },
        ),
        migrations.CreateModel(
            name='CharacterPower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', game_rules.fields.DotsField(default=1)),
                ('details', models.CharField(blank=True, max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powers', to='sheets.Character')),
                ('power', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game_rules.Power')),
                ('power_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game_rules.PowerOption', verbose_name='Option')),
            ],
            options={
                'verbose_name': 'Power',
            },
        ),
        migrations.CreateModel(
            name='DowntimeAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, editable=False, null=True)),
                ('player_request', models.TextField()),
                ('storyteller_response', models.TextField(blank=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downtime_actions', to='sheets.Character')),
                ('game_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downtime_actions', to='organization.GameEvent')),
            ],
            options={
                'verbose_name': 'Downtime Action',
            },
        ),
        migrations.CreateModel(
            name='SkillSpeciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(blank=True, choices=[('academics', 'Academics'), ('computer', 'Computer'), ('crafts', 'Crafts'), ('investigation', 'Investigation'), ('medicine', 'Medicine'), ('occult', 'Occult'), ('politics', 'Politics'), ('science', 'Science'), ('athletics', 'Athletics'), ('brawl', 'Brawl'), ('drive', 'Drive'), ('firearms', 'Firearms'), ('larceny', 'Larceny'), ('stealth', 'Stealth'), ('survival', 'Survival'), ('weaponry', 'Weaponry'), ('animal_ken', 'Animal Ken'), ('empathy', 'Empathy'), ('expression', 'Expression'), ('intimidation', 'Intimidation'), ('persuasion', 'Persuasion'), ('socialize', 'Socialize'), ('streetwise', 'Streetwise'), ('subterfuge', 'Subterfuge')], max_length=20)),
                ('speciality', models.CharField(blank=True, max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialities', to='sheets.Character')),
            ],
            options={
                'verbose_name': 'Skill Speciality',
                'verbose_name_plural': 'Skill Specialities',
            },
        ),
        migrations.AddField(
            model_name='approvalrequest',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_requests', to='sheets.Character'),
        ),
        migrations.AddField(
            model_name='approvalrequest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='approval_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='advancement',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience_awards', to='sheets.Character'),
        ),
        migrations.AddField(
            model_name='advancement',
            name='game_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience_awards', to='organization.GameEvent'),
        ),
    ]
