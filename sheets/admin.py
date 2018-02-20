from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django_object_actions import BaseDjangoObjectActions

from systems.models import PowerCategory, Power, SplatCategory, Splat
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
    min_num = 3
    extra = 0


@admin.register(Character)
class CharacterAdmin(BaseDjangoObjectActions, admin.ModelAdmin):
    model = Character
    inlines = (SkillSpecialityInline, MeritInline, )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', 'status'),
                ('user', 'organization', 'version')
            ),
        }),
        ('Template', {
            'fields': (
                ('primary_splat', 'secondary_splat',  'tertiary_splat',),
                ('primary_sub_splat', 'secondary_sub_splat', 'character_group', ),
                ('primary_anchor', 'secondary_anchor', 'concept', ),
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
                ('integrity', 'power_stat', 'resource',),
                ('size', 'health_levels', 'defense', ),
                ('speed', 'initiative', )
            ),
        }),
        ('Information', {
            'fields': (
                'background', 'alt_names',
            ),
        }),
    )
    list_display = ('name', 'template', 'user', 'organization', 'status')
    list_filter = ('template', )
    search_fields = ('name', 'user')
    readonly_fields = (
        'template', 'size', 'health_levels', 'speed',
        'initiative', 'defense', 'created', 'modified', 'version',
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
    change_actions = ('revision_this', )

    def revision_this(self, request, obj: Character):
        try:
            obj.create_revision()
            new_obj = obj.active_revision()
            return redirect('admin:sheets_character_change', object_id=new_obj.pk)
        except RuntimeError:
            pass

    revision_this.label = 'Create Revision'
    revision_this.short_description = 'Create a new revision'

    def get_change_actions(self, request, object_id, form_url):
        if not object_id:
            return []
        actions = super().get_change_actions(request, object_id, form_url)
        actions = list(actions)
        obj = Character.objects.get(pk=object_id)
        if obj.status != 'approved':
            actions.remove('revision_this')
        return actions

    def get_fieldsets(self, request, obj: Character=None):
        if obj is None:
            self.inlines = ()
            return (self.fieldsets[0], )
        else:
            self.inlines = CharacterAdmin.inlines + self.get_extra_inlines(request, obj)
        return self.fieldsets

    def get_extra_inlines(self, request, obj: Character):
        extra_inlines = []
        for category in PowerCategory.objects.filter(character_template=obj.template):

            class PowerInline(ParentInlineMixin):
                model = CharacterPower
                fields = ('power', 'rating', 'origin')
                readonly_fields = ('category', 'origin')
                power_category = category
                verbose_name = category.name
                verbose_name_plural = category.name
                extra = 0

                def get_queryset(self, request):
                    return CharacterPower.objects.filter(power__power_category=self.power_category)

                def get_field_queryset(self, db, db_field, request):
                    self.formset.power_category = self.power_category
                    queryset = super().get_field_queryset(db, db_field, request)
                    if db_field.name == 'power' and self.parent_obj:
                        return Power.objects.filter(power_category=self.power_category)
                    return queryset

                def origin(self, power: CharacterPower):
                    return f'{power.power.origin_splat}'

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
            for flavor, flavor_text in SplatCategory.FLAVORS:
                field = form.base_fields[flavor + '_splat']
                try:
                    category = SplatCategory.objects.get(flavor=flavor, character_template=obj.template)
                    field.queryset = Splat.objects.filter(splat_category=category)
                    field.label = category.name
                    if category.is_required and obj.template:
                        field.required = True
                except SplatCategory.DoesNotExist:
                    field.widget = HiddenInput()
            # Modify other template specific labels
            if obj.template:
                for trait in self.rename_traits:
                    label = getattr(obj.template, "{}_name".format(trait))
                    if label:
                        form.base_fields[trait].label = label
                    else:
                        form.base_fields[trait].widget = HiddenInput()
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields
        return self.readonly_fields_new

    def get_queryset(self, request):
        uuid = request.GET.get('uuid')
        if uuid:
            return Character.objects.filter(uuid=uuid)
        return Character.active.all()

    def get_list_display(self, request):
        uuid = request.GET.get('uuid')
        fields = list(super().get_list_display(request))
        if uuid:
            fields.append('version')
        return fields

#
