from django.contrib import admin
from sheets.models import *
from django.forms.widgets import HiddenInput


class ParentInlineMixin(admin.TabularInline):
    def __init__(self, parent_mode, admin_site):
        super().__init__(parent_mode, admin_site)
        self.parent_obj = None

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)


@admin.register(Chronicle)
class ChronicleAdmin(admin.ModelAdmin):
    model = Chronicle
    fields = (
        ('name', 'default_template'),
        ('theme', 'mood'),
        ('venue_storyteller', 'domain_storyteller'),
        ('venue_coordinator', 'domain_coordinator'),
        ('storytelling_group', 'coordinating_group'),
    )
    list_display = ('name', 'default_template', 'venue_storyteller', 'venue_coordinator')


class MeritInline(admin.TabularInline):
    model = CharacterMerit
    fields = ('merit', 'rating', 'detail', 'category', 'origin', )
    readonly_fields = ('category', 'origin', )
    extra = 0


class SkillSpecialityInline(admin.TabularInline):
    model = SkillSpeciality
    fields = ('speciality', 'skill')
    extra = 0


class ApprovalRequestInline(admin.TabularInline):
    model = ApprovalRequest
    fields = ('version', 'status', 'created_on', 'completed_on', 'details', 'spent_experience', )
    readonly_fields = ('version', 'created_on', 'completed_on',)
    can_delete = False
    max_num = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    model = Character
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
                ('storyteller_beats', 'organization_beats', 'created_on', ),
                ('spent_experience', 'available_experience', 'modified_on', ),
            ),
        }),
        ('Information', {
            'fields': (
                ('background',),
            ),
        }),
    )
    list_display = ('name', 'template', 'chronicle', 'player')
    list_filter = ('template', 'chronicle', )
    readonly_fields = (
        'template', 'size', 'health', 'speed', 'initiative', 'defense', 'version',
        'spent_experience', 'available_experience', 'created_on', 'modified_on',
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
            self.inlines = CharacterAdmin.inlines + self.get_extra_inlines(request, obj)
        return self.fieldsets

    def get_extra_inlines(self, request, obj: Character):
        extra_inlines = []
        for category in PowerCategory.objects.filter(template=obj.template):

            class PowerInline(ParentInlineMixin):
                model = CharacterPower
                fields = ('power', 'rating', 'detail', )
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


