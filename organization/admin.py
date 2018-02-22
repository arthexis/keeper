from django.contrib import admin

from core.admin import SimpleActionsModel
from core.models import UserProfile
from organization.models import Prestige, Membership, Domain, Chapter


class ProfileMemberInline(admin.TabularInline):
    model = Membership
    fields = ('chapter', 'title', 'status', 'external_id',)
    extra = 0


@admin.register(UserProfile)
class ProfileAdmin(SimpleActionsModel):
    model = UserProfile
    inlines = (ProfileMemberInline,)
    fields = (
        'username', 'email',
        'first_name', 'last_name',
        'phone', 'is_staff'
    )
    list_display = ('username', 'email', 'last_name', 'first_name', 'phone', 'is_staff')
    change_actions = ('change_password',)


class PrestigeInline(admin.TabularInline):
    model = Prestige
    fields = ('notes', 'amount', 'coordinator')
    extra = 0


class ChapterMemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'status', 'external_id',)
    extra = 1


class DomainInline(admin.StackedInline):
    model = Domain
    fields = ('name', 'rules_url',)
    extra = 0
    min_num = 1


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    model = Domain
    inlines = (DomainInline, ChapterMemberInline,)
    fields = ('name', 'rules_url',)
    list_display = ('name', 'rules_url', 'domains')

    def domains(self, obj: Chapter =None):
        if obj:
            return ','.join(obj.domains.values_list('name', flat=True))




