from django.contrib import admin
from core.admin import SimpleActionsModel

from game_rules.models import PowerCategory, Power, SplatCategory, Splat
from sheets.models import ApprovalRequest, Character, CharacterMerit, SkillSpeciality, CharacterPower
from django.forms.widgets import HiddenInput
from game_rules.admin import ParentInlineMixin
from game_rules.fields import DotsField, DotsInput


class MeritInline(admin.TabularInline):
    model = CharacterMerit
    fields = ('merit', 'rating', 'details', )
    extra = 0


class SkillSpecialityInline(admin.TabularInline):
    model = SkillSpeciality
    fields = ('speciality', 'skill')
    min_num = 3
    extra = 0
    verbose_name_plural = 'Specialities'
    verbose_name = 'Speciality'


class PendingApprovalInline(admin.TabularInline):
    model = ApprovalRequest
    fields = ('description', 'status', 'created', 'download_attachment_link')
    readonly_fields = ('created', 'download_attachment_link')
    verbose_name_plural = 'Pending Approvals'

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='pending')

    def download_attachment_link(self, obj=None):
        return obj.download_attachment_link() if obj else ''

    download_attachment_link.short_description = 'Attachment'


class ApprovalLogInline(admin.StackedInline):
    model = ApprovalRequest
    fields = ('description', 'created', 'modified')
    readonly_fields = ('created', 'modified', 'description')
    verbose_name_plural = 'Approval History'

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='complete')


class BasePowerInline(ParentInlineMixin):
    model = CharacterPower
    fields = ('power', 'rating', 'details' )
    readonly_fields = ('category',)
    power_category = None
    verbose_name = None
    verbose_name_plural = None
    extra = 0

    def get_queryset(self, request):
        return CharacterPower.objects.filter(power__power_category=self.power_category)

    def get_field_queryset(self, db, db_field, request):
        self.formset.power_category = self.power_category
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'power' and self.parent_obj:
            return Power.objects.filter(power_category=self.power_category)
        return queryset


@admin.register(Character)
class CharacterAdmin(SimpleActionsModel):
    model = Character
    inlines = (SkillSpecialityInline, MeritInline, )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', 'status'),
                ('user', 'domain', 'version'),
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
            ),
        }),
        ('Information', {
            'fields': (
                'background', 'alt_names',
            ),
        }),
    )
    list_display = ('name', 'template', 'user', 'domain', 'status')
    list_filter = ('template', )
    search_fields = ('name', 'user')
    readonly_fields = (
        'template', 'health_levels', 'created', 'modified', 'version',
    )
    readonly_fields_new = ('version', 'status',)
    formfield_overrides = {
        DotsField: {'widget': DotsInput}
    }
    rename_traits = (
        'power_stat', 'integrity', 'resource', 'primary_anchor',
        'secondary_anchor', 'character_group',
    )
    change_form_template = 'sheets/change_form.html'
    change_actions = (
        'create_revision',
    )

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

            class PowerInline(BasePowerInline):
                power_category = category
                verbose_name = category.name
                verbose_name_plural = category.name

            extra_inlines.append(PowerInline)

        if obj:
            approvals = obj.approval_requests
            if approvals.filter(status='pending').exists():
                extra_inlines.append(PendingApprovalInline)
            if approvals.filter(status='complete').exists():
                extra_inlines.append(ApprovalLogInline)

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


@admin.register(ApprovalRequest)
class ApprovalAdmin(admin.ModelAdmin):
    model = ApprovalRequest
    fields = ('get_character_link', 'description', 'created', 'download_attachment_link' )
    list_display = ('character', 'description', 'created', 'status')
    list_filter = ('status', )
    readonly_fields = ('created', 'get_character_link', 'download_attachment_link')
    search_fields = ('character', )

    def get_character_link(self, obj=None):
        if obj:
            return obj.get_character_link()

    get_character_link.short_description = "Character"
