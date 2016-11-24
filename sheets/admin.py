from django.contrib import admin
from sheets.models import *
from django.forms.widgets import HiddenInput


class ParentInlineMixin(admin.TabularInline):
    def __init__(self, parent_mode, admin_site):
        super().__init__(parent_mode, admin_site)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)


class MeritInline(admin.TabularInline):
    model = CharacterMerit
    fields = ('merit', 'rating', 'notes', 'category', 'origin', )
    readonly_fields = ('category', 'origin', )
    extra = 0


class PowerInline(ParentInlineMixin):
    model = CharacterPower
    fields = ('power', 'rating', 'category', )
    readonly_fields = ('category', )
    extra = 0

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'power' and self.parent_obj:
            return Power.objects.filter(category__template=self.parent_obj.template)
        return queryset


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    model = Character
    inlines = (MeritInline, PowerInline )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', ),
            ),
        }),
        ('Template', {
            'fields': (
                ('primary_splat', 'secondary_splat', 'tertiary_splat', ),
                ('primary_anchor', 'secondary_anchor', ),
                ('power_stat', 'integrity', 'resource', ),
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
        ('Information', {
            'fields': (
                ('background'),
            ),
        }),
    )
    list_display = ('name', 'template', )
    list_filter = ('template', )
    formfield_overrides = {
        DotsField: {'widget': DotsInput}
    }

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (self.fieldsets[0], )
        return self.fieldsets

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
                form.base_fields['power_stat'].label = obj.template.power_stat_name
                form.base_fields['integrity'].label = obj.template.integrity_name
                form.base_fields['resource'].label = obj.template.resource_name
                form.base_fields['primary_anchor'].label = obj.template.primary_anchor_name
                form.base_fields['secondary_anchor'].label = obj.template.secondary_anchor_name
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('template', )

