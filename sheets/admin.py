from django.contrib import admin

from systems.models import PowerCategory, Power, Splat, SplatOption
from sheets.models import *
from django.forms.widgets import HiddenInput
from systems.admin import ParentInlineMixin
from systems.fields import DotsField, DotsInput


class MeritInline(admin.TabularInline):
    model = CharacterMerit
    fields = ('merit', 'rating', 'details', 'origin', )
    readonly_fields = ('origin', )
    extra = 0


class SkillSpecialityInline(admin.TabularInline):
    model = SkillSpeciality
    fields = ('speciality', 'skill')
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    model = Character
    inlines = (SkillSpecialityInline, MeritInline, )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', ),
                ('user', 'organization')
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
                ('size', 'health_levels', 'defense', ),
                ('speed', 'initiative', )
            ),
        }),
        ('Information', {
            'fields': (
                ('background',),
            ),
        }),
    )
    list_display = ('name', 'template',)
    list_filter = ('template', )
    search_fields = ('name', 'user')
    readonly_fields = (
        'template', 'size', 'health_levels', 'speed', 'initiative', 'defense', 'created_on', 'modified_on',
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

        return tuple(extra_inlines)

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

#
