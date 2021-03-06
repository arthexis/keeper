from django.contrib import admin
from django.urls import reverse

from game_rules.models import Splat, SplatCategory, Merit, Power, PowerCategory, CharacterTemplate, TemplateAnchor, \
    PowerOption, MeritVariant
from core.admin import SaveRedirectAdmin, HiddenAdmin


class ParentInlineMixin(admin.TabularInline):
    field_querysets = []

    def __init__(self, parent_mode, admin_site):
        super().__init__(parent_mode, admin_site)
        self.parent_obj = None

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        if self.parent_obj:
            for target in self.field_querysets:
                if db_field.name == target:
                    return getattr(self, f'get_{target}_queryset')(request, qs=None)
        return qs


class SplatInline(admin.TabularInline):
    model = Splat
    fields = ('name', )
    min_num = 1
    extra = 0


class SplatCategoryInline(admin.TabularInline):
    model = SplatCategory
    fields = ('name', 'flavor', 'splats')
    readonly_fields = ('splats', )
    extra = 0
    show_change_link = True
    max_num = 5

    def splats(self, obj=None):
        return obj.splat_names()


@admin.register(SplatCategory)
class SplatCategoryAdmin(SaveRedirectAdmin, HiddenAdmin):
    model = SplatCategory
    list_display = ('name', 'character_template', 'splat_names', )
    readonly_fields = ('splat_names', )
    inlines = (SplatInline, )
    fields = ('name', 'character_template', 'flavor', 'is_required', )

    def get_save_redirect_url(self, request, obj):
        return reverse('admin:game_rules_charactertemplate_change', args=[obj.character_template.pk])


class MeritVariantInline(admin.TabularInline):
    model = MeritVariant
    fields = ('dots', 'name')
    max_num = 5
    min_num = 5


@admin.register(Merit)
class MeritAdmin(admin.ModelAdmin):
    model = Merit
    fields = (('name', 'reference_code'), )
    list_display = ('name', )
    prepopulated_fields = {'reference_code': ('name', )}
    search_fields = ('name', )
    inlines = (MeritVariantInline, )


@admin.register(Power)
class PowerAdmin(admin.ModelAdmin):
    model = Power
    fields = (('name', 'power_category'),)
    list_display = ('name', 'power_category', 'character_template')
    list_filter = ('power_category', )


class PowerInline(admin.TabularInline):
    model = Power
    fields = ('name', )
    extra = 0
    show_change_link = True


class PowerOptionInline(admin.TabularInline):
    model = PowerOption
    fields = ('name',)
    extra = 0
    show_change_link = True


@admin.register(PowerCategory)
class PowerCategoryAdmin(SaveRedirectAdmin, HiddenAdmin):
    model = PowerCategory
    fields = ('name', 'character_template')
    list_display = ('name', 'character_template', 'power_names', )
    readonly_fields = ('power_names', )
    inlines = (PowerOptionInline, PowerInline, )

    def get_save_redirect_url(self, request, obj):
        return reverse('admin:game_rules_charactertemplate_change', args=[obj.character_template.pk])


class PowerCategoryInline(admin.TabularInline):
    model = PowerCategory
    fields = ('name', 'power_names',)
    readonly_fields = ('power_names',)
    extra = 0
    show_change_link = True


class TemplateAnchorInline(admin.TabularInline):
    model = TemplateAnchor
    fields = ('name', )
    extra = 0
    show_change_link = True


@admin.register(CharacterTemplate)
class CharacterTemplateAdmin(admin.ModelAdmin):
    model = CharacterTemplate
    list_display = ('name', 'game_line', 'power_stat_name', 'integrity_name', 'resource_name')
    fieldsets = (
        ('Information', {
            'fields': (
                ('name', 'game_line',),
                ('integrity_name', 'power_stat_name',),
                ('resource_name', 'character_group_name',),
                ('primary_anchor_name', 'secondary_anchor_name',),
            ),
        }),
        ('Configuration', {
            'fields': ('reference_code',)
        })
    )
    inlines = (SplatCategoryInline, PowerCategoryInline, TemplateAnchorInline)
    prepopulated_fields = {'reference_code': ('name', 'game_line')}
