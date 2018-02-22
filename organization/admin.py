from django.contrib import admin

from core.admin import SimpleActionsModel
from core.models import UserProfile
from organization.models import Prestige, Membership, Domain, Chapter


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
    list_display_links = ('username',)
    change_actions = ('change_password',)


class PrestigeInline(admin.TabularInline):
    model = Prestige
    fields = ('notes', 'amount', 'witness')
    extra = 0


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    inlines = (PrestigeInline, )
    fields = ('user', 'chapter', 'title', 'external_id', 'status')
    list_display = ('user', 'chapter', 'title', 'status', 'external_id', )
    list_editable = ('title', 'status', 'external_id', )
    list_display_links = ('user', 'chapter')
    list_filter = ('status', 'title')


class MemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'status', 'external_id',)
    extra = 1
    show_change_link = True


class DomainInline(admin.StackedInline):
    model = Domain
    fields = ('name', 'reference_code', 'information',)
    extra = 0
    min_num = 1


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    model = Domain
    fields = ('name', 'reference_code', 'information', )
    list_display = ('name', 'reference_code', )
    prepopulated_fields = {'reference_code': ('name', )}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    model = Domain
    inlines = (DomainInline, MemberInline, )
    fields = ('name', 'reference_code', 'information',)
    list_display = ('name', 'reference_code',)
    prepopulated_fields = {'reference_code': ('name',)}




