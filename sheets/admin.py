from django.contrib import admin, messages

from core.admin import SimpleActionsModel

from sheets.forms import CharacterAdminForm
from game_rules.models import PowerCategory, Power, SplatCategory, Splat, TemplateAnchor, PowerOption
from sheets.models import ApprovalRequest, Character, CharacterMerit, SkillSpeciality, CharacterPower, \
    CharacterAnchor, Advancement, DowntimeAction
from django.forms.widgets import HiddenInput
from game_rules.admin import ParentInlineMixin
from game_rules.fields import DotsField
from game_rules.widgets import DotsInput


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


class BaseApprovalMixin:

    def download_attachment_link(self, obj=None):
        return obj.download_attachment_link() if obj else ''

    def has_add_permission(self, request):
        return False

    show_change_link = True
    download_attachment_link.short_description = 'Attachment'


class PendingApprovalInline(BaseApprovalMixin, admin.StackedInline):
    model = ApprovalRequest
    fields = (
        ('base_experience_cost', 'prestige_level'), ('quantity', 'total_experience_cost'),
        'detail', 'additional_info', 'created', 'download_attachment_link'
    )
    readonly_fields = ('created', 'download_attachment_link', 'total_experience_cost')
    verbose_name_plural = 'Pending Approvals'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='pending')


class ApprovalLogInline(BaseApprovalMixin, admin.TabularInline):

    # TODO Add link to view original revision

    model = ApprovalRequest
    fields = ('detail', 'total_experience_cost', 'modified', 'download_attachment_link')
    readonly_fields = (
        'total_experience_cost', 'modified', 'detail', 'download_attachment_link')
    verbose_name_plural = 'Approval History'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='complete')


class AdvancementInline(admin.TabularInline):
    model = Advancement
    fields = ('created', 'game_event', 'experience', 'beats', 'notes')
    readonly_fields = ('created', )
    extra = 0


class DowntimeActionInline(admin.StackedInline):
    model = DowntimeAction
    fields = ('game_event', 'player_request', 'storyteller_response', )
    extra = 0


class BasePowerInline(ParentInlineMixin):
    model = CharacterPower
    fields = ('power', 'power_option', 'rating', 'details')
    readonly_fields = ('category',)
    power_category = None
    verbose_name = None
    verbose_name_plural = None
    extra = 0

    def get_queryset(self, request):
        return CharacterPower.objects.filter(power__power_category=self.power_category)

    def get_field_queryset(self, db, db_field, request):
        self.formset.power_category = self.power_category
        if db_field.name == 'power' and self.parent_obj:
            return Power.objects.filter(power_category=self.power_category)
        if db_field.name == 'power_option' and self.parent_obj:
            return PowerOption.objects.filter(power_category=self.power_category)
        return super().get_field_queryset(db, db_field, request)


class BaseAnchorInline(ParentInlineMixin):
    model = CharacterAnchor
    fields = ('template_anchor', 'value')
    character_template = None
    extra = 0
    field_querysets = ('template_anchor', )

    def get_template_anchor_queryset(self, request, qs=None):
        return TemplateAnchor.objects.filter(character_template=self.character_template)


@admin.register(Character)
class CharacterAdmin(SimpleActionsModel):
    model = Character
    form = CharacterAdminForm
    inlines = (SkillSpecialityInline, MeritInline,)
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', 'status'),
                ('user', 'chronicle', 'version'),
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
            'description': "If left blank, advantages will be calculated automatically on save.",
            'fields': (
                ('integrity', 'power_stat', 'resource_max',),
                ('willpower', 'health', 'resource_start'),
                ('size', 'speed', 'initiative'),
            ),
        }),
        ('Information', {
            'fields': (
                'storyteller_notes', 'player_notes',
            ),
        }),
    )
    list_display = ('name', 'template', 'user', 'chronicle', 'status')
    list_filter = ('template', )
    search_fields = ('name', 'user')
    readonly_fields = (
        'template', 'created', 'modified', 'version',
    )
    readonly_fields_new = ('version', 'status',)
    formfield_overrides = {
        DotsField: {'widget': DotsInput},
    }
    rename_traits = (
        'power_stat', 'integrity', 'primary_anchor',
        'secondary_anchor', 'character_group',
        ('resource_max', 'resource_name', lambda x: f'{x} Capacity'),
        ('resource_start', 'resource_name', lambda x: f'Starting {x}')
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
            class AnchorInline(BaseAnchorInline):
                character_template = obj.template
            extra_inlines.append(AnchorInline)

            approvals = obj.approval_requests
            if approvals.filter(status='pending').exists():
                extra_inlines.append(PendingApprovalInline)
            if approvals.filter(status='complete').exists():
                extra_inlines.append(ApprovalLogInline)

            extra_inlines.append(AdvancementInline)
            extra_inlines.append(DowntimeActionInline)

        return tuple(extra_inlines)

    def save_model(self, request, obj: Character, form, change):
        super().save_model(request, obj, form, change)

        # If there is no existing approval on save, create an initial approval
        manager = ApprovalRequest.objects
        if not manager.filter(character=obj).exists():
            approval = manager.create(character=obj, user=obj.user, description='Initial Approval')
            if obj.status == 'approved':
                approval.status = 'complete'
                approval.save()
            messages.info(request, 'Initial Approval request created automatically')

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
                    if isinstance(trait, str):
                        trait_name = f'{trait}_name'
                        label = getattr(obj.template, trait_name)
                    else:
                        trait, trait_name, func = trait
                        label = func(getattr(obj.template, trait_name))
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
    fields = (
        'character',
        'get_character_link',
        ('base_experience_cost', 'prestige_level'),
        ('quantity', 'total_experience_cost'),
        'detail',
        'additional_info',
        ('created', 'modified'),
        'download_attachment_link',
        'status'
    )
    list_display = ('character', 'user', 'detail', 'created', 'status')
    list_filter = ('status', )
    readonly_fields = (
        'created', 'get_character_link', 'modified',
        'download_attachment_link', 'status', 'total_experience_cost')
    search_fields = ('character', 'user', 'detail')

    def get_character_link(self, obj=None):
        if obj:
            return obj.get_character_link(full=True)

    get_character_link.short_description = "Edit Character"
