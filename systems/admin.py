from django.contrib import admin

from systems.models import *


class SplatInline(admin.TabularInline):
    model = SplatOption
    fields = ('name', 'reference_book', 'reference_page')
    min_num = 1
    extra = 0


@admin.register(Splat)
class SplatCategoryAdmin(admin.ModelAdmin):
    model = Splat
    list_display = ('name', 'template', 'splat_names')
    readonly_fields = ('splat_names', )
    inlines = (SplatInline, )
    fieldsets = (
        (None, {
            'fields': (
                ('name',),
                ('template', 'flavor', ),
            ),
        }),
    )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    model = Template
    list_display = ('name', 'power_stat_name', 'integrity_name', 'resource_name')
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'alias',),
                ('integrity_name', 'power_stat_name',),
                ('resource_name', 'character_group_name',),
                ('primary_anchor_name', 'secondary_anchor_name',),
            ),
        }),
    )


@admin.register(Merit)
class MeritAdmin(admin.ModelAdmin):
    model = Merit
    fields = ('name', 'category', 'template', 'reference_book', 'reference_page', )
    list_display = ('name', 'category', 'template', )


class PowerInline(admin.TabularInline):
    model = Power
    fields = ('name', 'reference_book', 'reference_page')
    extra = 1


@admin.register(PowerCategory)
class PowerCategoryAdmin(admin.ModelAdmin):
    model = PowerCategory
    fields = ('name', 'template')
    list_display = ('name', 'template', 'power_names', )
    readonly_fields = ('power_names', )
    inlines = (PowerInline, )

