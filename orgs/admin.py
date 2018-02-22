from django.contrib import admin

from core.admin import SimpleActionsModel
from orgs.models import UserProfile, Event, Prestige, Membership, Organization


@admin.register(UserProfile)
class ProfileAdmin(SimpleActionsModel):
    model = UserProfile
    fields = (
        'username', 'email',
        'first_name', 'last_name',
        'phone', 'is_staff'
    )
    list_display = ('username', 'email', 'last_name', 'phone')
    list_editable = ('email', 'last_name', 'phone')
    list_display_links = ('username', )
    change_actions = ('change_password', )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('name', 'event_date')


class PrestigeInline(admin.TabularInline):
    model = Prestige
    fields = ('notes', 'amount', 'witness')
    extra = 0


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    inlines = (PrestigeInline, )
    fields = ('user', 'organization', 'title', 'external_id', 'status')
    list_display = ('user', 'organization', 'title', 'status', 'external_id', )
    list_editable = ('title', 'status', 'external_id', )
    list_display_links = ('user', 'organization')
    list_filter = ('status', 'title')


class MemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'status', 'external_id',)
    extra = 1
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    fields = ('name', 'reference_code', 'information', )
    list_display = ('name', 'reference_code', )
    inlines = (MemberInline, )
    prepopulated_fields = {'reference_code': ('name', )}


class OrganizationInline(admin.TabularInline):
    model = Organization
    fields = ('name', 'reference_code')




