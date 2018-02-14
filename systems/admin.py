from django.contrib import admin
from systems.models import *


class ParentInlineMixin(admin.TabularInline):
    def __init__(self, parent_mode, admin_site):
        super().__init__(parent_mode, admin_site)
        self.parent_obj = None

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)


class SplatOptionInline(admin.TabularInline):
    model = SplatOption
    fields = ('name', )
    min_num = 1
    extra = 0


class SplatInline(admin.TabularInline):
    model = Splat
    fields = ('name', 'flavor', 'options')
    readonly_fields = ('options', )
    min_num = 1
    max_num = 3
    extra = 0
    show_change_link = True

    def options(self, obj=None):
        return obj.get_options_str()


@admin.register(Splat)
class SplatCategoryAdmin(admin.ModelAdmin):
    model = Splat
    list_display = ('name', 'template', 'splat_names')
    readonly_fields = ('splat_names', )
    fieldsets = (
        (None, {
            'fields': (
                ('name',),
                ('template', 'flavor', ),
            ),
        }),
    )


@admin.register(Merit)
class MeritAdmin(admin.ModelAdmin):
    model = Merit
    fields = ('name', 'template', )
    list_display = ('name', 'template', )


class PowerInline(admin.TabularInline):
    model = Power
    fields = ('name',)
    extra = 0
    show_change_link = True


@admin.register(PowerCategory)
class PowerCategoryAdmin(admin.ModelAdmin):
    model = PowerCategory
    fields = ('name', 'template')
    list_display = ('name', 'template', 'power_names', )
    readonly_fields = ('power_names', )
    inlines = (PowerInline, )


class PowerCategoryInline(admin.TabularInline):
    model = PowerCategory
    fields = ('name',)
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
    inlines = (SplatInline, PowerCategoryInline)
    prepopulated_fields = {'reference_code': ('name', 'game_line')}

