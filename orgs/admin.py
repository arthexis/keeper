from django.contrib import admin
from orgs.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    fields = ('user', 'phone', 'information')
    list_display = ('username', 'email', 'first_name', 'last_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('name', 'event_date')


class MemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'is_officer', 'is_active')
    extra = 1
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    fields = ('name', 'parent_org', 'is_public', 'information', 'reference_code')
    list_display = ('name', 'parent_org', 'is_public')
    inlines = (MemberInline, )
    prepopulated_fields = {'reference_code': ('name', )}
