from django.contrib import admin

from core.admin import SimpleActionsModel
from core.models import UserProfile
from organization.models import Prestige, Membership, Domain, Chapter, PrestigeReport, PrestigeLevel, Invitation
from keeper.utils import missing


class ProfileMemberInline(admin.TabularInline):
    model = Membership
    fields = ('chapter', 'title', 'status', 'external_id', 'prestige_level')
    readonly_fields = ('prestige_level', )
    extra = 0


@admin.register(UserProfile)
class ProfileAdmin(SimpleActionsModel):
    model = UserProfile
    inlines = (ProfileMemberInline,)
    fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_display = ('username', 'email', 'last_name', 'first_name', 'phone', 'is_staff')
    change_actions = ('change_password',)


class ChapterMemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'status', 'external_id', 'prestige_level')
    readonly_fields = ('prestige_level',)
    extra = 1


class DomainInline(admin.StackedInline):
    model = Domain
    fields = ('name', 'rules_url', 'chronicle_name', 'short_description')
    extra = 0
    min_num = 1


class PrestigeLevelInline(admin.TabularInline):
    model = PrestigeLevel
    fields = ('level', 'prestige_required')
    min_num = 0
    extra = 1


class InviteInline(admin.TabularInline):
    model = Invitation
    fields = ('email_address', 'external_id', 'invite_link')
    readonly_fields = ('invite_link', )
    extra = 3
    min_num = 0

    @missing('-- Save to generate link --')
    def invite_link(self, obj: Invitation=None):
        return obj.invite_link()


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    model = Domain
    inlines = (DomainInline, PrestigeLevelInline, ChapterMemberInline, InviteInline)
    fields = ('name', 'rules_url', 'site')
    list_display = ('name', 'rules_url', 'domains')

    def domains(self, obj: Chapter =None):
        if obj:
            return ','.join(obj.domains.values_list('name', flat=True))


class ReportPrestigeInline(admin.TabularInline):
    model = Prestige
    fields = ('membership', 'amount', 'notes')
    extra = 3
    min_num = 1


@admin.register(PrestigeReport)
class PrestigeReport(admin.ModelAdmin):
    model = PrestigeReport
    inlines = (ReportPrestigeInline,)
    fields = ('chapter', 'start', 'end')



