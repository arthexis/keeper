from django.contrib import admin
from django.urls import reverse

from systems.models import Splat, SplatCategory, Merit, Power, PowerCategory, CharacterTemplate
from admin_tech.admin import SaveRedirectAdmin


class ParentInlineMixin(admin.TabularInline):
    def __init__(self, parent_mode, admin_site):
        super().__init__(parent_mode, admin_site)
        self.parent_obj = None

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)


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
class SplatCategoryAdmin(SaveRedirectAdmin):
    model = SplatCategory
    list_display = ('name', 'character_template', 'splat_names', )
    readonly_fields = ('splat_names', )
    inlines = (SplatInline, )
    fields = ('name', 'character_template', 'flavor', 'is_required', )

    def get_save_redirect_url(self, request, obj):
        return reverse('admin:systems_charactertemplate_change', args=[obj.character_template.pk])


@admin.register(Merit)
class MeritAdmin(admin.ModelAdmin):
    model = Merit
    fields = (('name', 'reference_code'), )
    list_display = ('name', )
    # list_editable = ('category', 'character_template', )
    # list_display_links = ('name', )
    prepopulated_fields = {'reference_code': ('name', )}


# @admin.register(Power)
# class PowerAdmin(admin.ModelAdmin):
#     model = Power
#     fields = ('name', 'power_category',)
#     list_filter = ('power_category', )
#     list_display = ('name', 'power_category', )


class PowerInline(admin.TabularInline):
    model = Power
    fields = ('name', )
    extra = 0
    show_change_link = True


@admin.register(PowerCategory)
class PowerCategoryAdmin(SaveRedirectAdmin):
    model = PowerCategory
    fields = ('name', 'character_template')
    list_display = ('name', 'character_template', 'power_names', )
    readonly_fields = ('power_names', )
    inlines = (PowerInline, )

    def get_save_redirect_url(self, request, obj):
        return reverse('admin:systems_charactertemplate_change', args=[obj.character_template.pk])


class PowerCategoryInline(admin.TabularInline):
    model = PowerCategory
    fields = ('name', 'power_names', )
    readonly_fields = ('power_names', )
    extra = 0
    show_change_link = True


@admin.register(CharacterTemplate)
class TemplateAdmin(admin.ModelAdmin):
    model = CharacterTemplate
    list_display = ('name', 'game_line', 'power_stat_name', 'integrity_name', 'resource_name')
    fieldsets = (
        ('Information', {
            'fields': (
                ('name', 'game_line',),
                ('integrity_name', 'power_stat_name',),
                ('resource_name', 'character_group_name',),
                ('primary_anchor_name', 'secondary_anchor_name',),
                ('experiences_prefix',),
            ),
        }),
        ('Configuration', {
            'fields': ('reference_code',)
        })
    )
    inlines = (SplatCategoryInline, PowerCategoryInline)
    prepopulated_fields = {'reference_code': ('name', 'game_line')}

