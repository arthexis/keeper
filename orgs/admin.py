from django.contrib import admin
from orgs.models import Profile, Event, Prestige, Membership, Organization


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        'phone',
        'information'
    )
    list_display = ('username', 'email', 'last_name', 'phone')
    list_editable = ('email', 'last_name', 'phone')
    list_display_links = ('username', )


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
    fields = (
        'user', 'organization', 'title',
        ('is_active', 'is_officer'), ('is_owner', 'is_blocked'),
    )
    list_display = ('user', 'organization', 'title', 'is_active', 'is_officer', 'is_owner', 'is_blocked')
    list_editable = ('title', 'is_active', 'is_officer', 'is_owner', 'is_blocked')
    list_display_links = ('user', 'organization')
    list_filter = ('is_active', 'is_officer', 'is_owner', 'is_blocked')


class MemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'is_officer', 'is_active', 'is_blocked', 'is_owner')
    extra = 1
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    fields = ('name', 'parent_org', 'is_public', 'information', 'reference_code')
    list_display = ('name', 'parent_org', 'is_public')
    inlines = (MemberInline, )
    prepopulated_fields = {'reference_code': ('name', )}
