from django.contrib import admin
from sheets.models import *
from django.forms.widgets import HiddenInput
from easy_select2 import select2_modelform


class ParentInlineMixin(admin.TabularInline):
    def __init__(self, parent_mode, admin_site):
        super().__init__(parent_mode, admin_site)
        self.parent_obj = None

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)


class PrestigeInline(admin.TabularInline):
    model = Prestige
    extra = 0
    fields = ('prestige_beats', 'details', 'awarded_on')
    readonly_fields = ('awarded_on', )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    fields = (
        ('user', 'status'),
        ('joined_on', 'starts_on', 'ends_on'),
        ('phone', )
    )
    list_display = ('user_name', 'user_email', 'status', 'prestige_level')
    inlines = (PrestigeInline, )


class EventInline(admin.TabularInline):
    model = Event
    fields = ('name', 'event_date', 'planning_document')
    extra = 0
    show_change_link = True


@admin.register(Chronicle)
class ChronicleAdmin(admin.ModelAdmin):
    model = Chronicle
    inlines = (EventInline, )
    fields = (
        ('name', 'code'),
        ('default_template', ),
        ('theme', 'mood'),
        ('venue_storyteller', 'domain_storyteller'),
        ('venue_coordinator', 'domain_coordinator'),
        ('storytelling_group', 'coordinating_group'),
    )
    list_display = ('name', 'code', 'default_template', 'venue_storyteller', 'venue_coordinator')


class MeritInline(admin.TabularInline):
    model = CharacterMerit
    form = select2_modelform(CharacterMerit, attrs={'width': '200px'})
    fields = ('merit', 'rating', 'details', 'category', 'origin', )
    readonly_fields = ('category', 'origin', )
    extra = 0


class SkillSpecialityInline(admin.TabularInline):
    model = SkillSpeciality
    form = select2_modelform(SkillSpeciality, attrs={'width': '180px'})
    fields = ('speciality', 'skill')
    extra = 0


class ApprovalRequestInline(admin.TabularInline):
    model = ApprovalRequest
    fields = ('version', 'status', 'created_on', 'completed_on', 'details', 'spent_experience', )
    readonly_fields = ('version', 'created_on', 'completed_on',)
    can_delete = False
    max_num = 0


class EventAssistanceInline(admin.TabularInline):
    model = Assistance
    fields = ('character', 'storyteller_beats', 'coordinator_beats', 'details')
    extra = 0


class CharacterAssistanceInline(admin.TabularInline):
    model = Assistance
    fields = ('event', 'storyteller_beats', 'coordinator_beats', 'details')
    extra = 0


class CharacterDowntimeInline(admin.TabularInline):
    model = Downtime
    show_change_link = True
    fields = ('event', 'sent_on', 'is_resolved')
    readonly_fields = ('sent_on', )
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    model = Character
    form = select2_modelform(Character, attrs={'width': '180px'})
    inlines = (SkillSpecialityInline, MeritInline, )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', ),
                ('player', 'chronicle', 'version'),
            ),
        }),
        ('Template', {
            'fields': (
                ('primary_splat', 'secondary_splat', 'tertiary_splat', ),
                ('primary_anchor', 'secondary_anchor', 'concept', ),
                ('faction', 'character_group', ),
            ),
        }),
        ('Attributes', {
            'fields': (
                ('intelligence', 'strength', 'presence', ),
                ('wits', 'dexterity', 'manipulation', ),
                ('resolve', 'stamina', 'composure', ),
            ),
        }),
        ('Skills', {
            'fields': (
                ('academics', 'athletics', 'animal_ken'),
                ('computer', 'brawl', 'empathy'),
                ('crafts', 'drive', 'expression'),
                ('investigation', 'firearms', 'intimidation'),
                ('medicine', 'larceny', 'persuasion'),
                ('occult', 'stealth', 'socialize'),
                ('politics', 'survival', 'streetwise'),
                ('science', 'weaponry', 'subterfuge'),
            ),
        }),
        ('Advantages', {
            'fields': (
                ('power_stat', 'integrity', 'resource',),
                ('size', 'health', 'defense', ),
                ('speed', 'initiative', )
            ),
        }),
        ('Character Advancement', {
            'fields': (
                ('storyteller_beats', 'coordinator_beats', 'prestige_beats', ),
                ('accumulated_experience', 'spent_experience', 'available_experience', ),
                ('created_on', 'modified_on',)
            ),
        }),
        ('Information', {
            'fields': (
                ('background',),
            ),
        }),
    )
    list_display = ('name', 'template', 'chronicle', 'player_name', 'player_email')
    list_filter = ('template', )
    search_fields = ('name', 'player_name', 'player_email', 'player')
    readonly_fields = (
        'template', 'size', 'health', 'speed', 'initiative', 'defense', 'version',
        'spent_experience', 'available_experience', 'created_on', 'modified_on',
        'storyteller_beats', 'coordinator_beats', 'prestige_beats', 'accumulated_experience',
    )
    readonly_fields_new = ('version', )
    formfield_overrides = {
        DotsField: {'widget': DotsInput}
    }
    rename_traits = (
        'power_stat', 'integrity', 'resource', 'primary_anchor',
        'secondary_anchor', 'character_group',
    )
    change_form_template = 'sheets/change_form.html'

    def get_fieldsets(self, request, obj: Character=None):
        if obj is None:
            self.inlines = ()
            return (self.fieldsets[0], )
        else:
            self.inlines = CharacterAdmin.inlines + \
                           self.get_extra_inlines(request, obj) + \
                           (CharacterAssistanceInline, CharacterDowntimeInline)
        return self.fieldsets

    def get_extra_inlines(self, request, obj: Character):
        extra_inlines = []
        for category in PowerCategory.objects.filter(template=obj.template):

            class PowerInline(ParentInlineMixin):
                model = CharacterPower
                form = select2_modelform(CharacterPower, attrs={'width': '200px'})
                fields = ('power', 'rating', 'details', )
                readonly_fields = ('category', )
                power_category = category
                verbose_name = category.name
                verbose_name_plural = category.name
                extra = 0

                def get_queryset(self, request):
                    return CharacterPower.objects.filter(power__category=self.power_category)

                def get_field_queryset(self, db, db_field, request):
                    self.formset.power_category = self.power_category
                    queryset = super().get_field_queryset(db, db_field, request)
                    if db_field.name == 'power' and self.parent_obj:
                        return Power.objects.filter(category=self.power_category)
                    return queryset

            extra_inlines.append(PowerInline)

        return tuple(extra_inlines) + (ApprovalRequestInline,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(formset, "power_category"):
                instance.category = formset.power_category
            instance.save()
        formset.save_m2m()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            # Rename splats and filter their choices
            for flavor in ('primary', 'secondary', 'tertiary'):
                field = form.base_fields[flavor + '_splat']
                try:
                    category = Splat.objects.get(flavor=flavor, template=obj.template)
                    field.queryset = SplatOption.objects.filter(category=category)
                    field.label = category.name
                    if flavor == 'primary' and obj.template:
                        field.required = True
                except Splat.DoesNotExist:
                    field.widget = HiddenInput()
            # Modify other template specific labels
            if obj.template:
                for trait in self.rename_traits:
                    form.base_fields[trait].label = getattr(obj.template, "{}_name".format(trait))
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields
        return self.readonly_fields_new


@admin.register(PendingApproval)
class PendingApprovalAdmin(admin.ModelAdmin):
    model = PendingApproval
    list_display = ('request_id', 'chronicle', 'character', 'created_on', 'summary', )
    search_fields = ('character', '`player_name', 'player_email', )
    fieldsets = (
        (None, {
            'fields': (
                ('character', 'status', ),
                ('spent_experience', 'created_on', ),
                ('details', ),
            ),
        }),
    )
    readonly_fields = ('version', 'created_on', )

    def get_readonly_fields(self, request, obj=None):
        fields = self.readonly_fields
        if obj:
            fields += ('character', )
        if not obj or not obj.can_approve(request.user):
            return fields + ('status', )
        return fields


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('short_name', 'event_date', 'chronicle', 'name')
    inlines = (EventAssistanceInline, )


class AspirationInline(admin.StackedInline):
    model = Aspiration
    min_num = 3
    max_num = 3
    fields = ('downtime', 'category', 'player_aspiration', 'storyteller_response')


@admin.register(Downtime)
class DowntimeAdmin(admin.ModelAdmin):
    model = Downtime
    list_display = ('chronicle', 'event', 'character', 'sent_on', 'is_resolved')
    search_fields = ('event', 'character')
    list_filter = ('event__chronicle', 'is_resolved')
    inlines = (AspirationInline, )


