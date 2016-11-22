from django.contrib import admin

from systems.models import *


class SplatInline(admin.TabularInline):
    model = Splat
    fields = ('name', 'alias', 'description', 'is_playable')
    min_num = 5
    extra = 0


@admin.register(SplatCategory)
class SplatCategoryAdmin(admin.ModelAdmin):
    model = SplatCategory
    list_display = ('name', 'template', 'splat_names')
    readonly_fields = ('splat_names', )
    inlines = (SplatInline, )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'template', ),
                ('is_required', 'is_editable', ),
            ),
        }),
    )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    model = Template
    list_display = ('name', 'alias', 'power_stat_name', 'integrity_name', 'resource_name')
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'alias'),
                ('integrity_name', 'power_stat_name', 'resource_name'),
            ),
        }),
    )

