from django.contrib import admin

from core.admin import SimpleActionsModel, CSVImportInline
from core.models import UserProfile
from organization.models import Prestige, Membership, Chronicle, Organization, PrestigeReport, PrestigeLevel, \
    Invitation, GameEvent
from sheets.models import Advancement
from keeper.utils import missing


class ProfileMemberInline(admin.TabularInline):
    model = Membership
    fields = ('organization', 'title', 'status', 'external_id', 'prestige_level')
    readonly_fields = ('prestige_level', )
    extra = 0


@admin.register(UserProfile)
class ProfileAdmin(SimpleActionsModel):
    model = UserProfile
    inlines = (ProfileMemberInline,)
    fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_display = ('username', 'email', 'last_name', 'first_name', 'phone', 'is_staff')
    change_actions = ('change_password',)


class OrganizationMemberInline(admin.TabularInline):
    model = Membership
    fields = ('user', 'title', 'status', 'external_id', 'prestige_level')
    readonly_fields = ('prestige_level',)
    extra = 1


class ChronicleInline(admin.TabularInline):
    model = Chronicle
    fields = ('name', 'reference_code', )
    extra = 0
    min_num = 1


class PrestigeLevelInline(admin.TabularInline):
    model = PrestigeLevel
    fields = ('level',  'name', 'prestige_required')
    min_num = 0
    extra = 1


class InviteInline(CSVImportInline):
    model = Invitation
    fields = ('email_address', 'external_id', 'invite_link')
    readonly_fields = ('invite_link', )
    extra = 1
    min_num = 0
    upload_fields = ['email_address', 'external_id']

    @missing('-- Save to generate link --')
    def invite_link(self, obj: Invitation=None):
        return obj.invite_link()


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Chronicle
    inlines = (ChronicleInline, PrestigeLevelInline, OrganizationMemberInline, InviteInline)
    fields = ('name', 'site', 'reference_code', )
    list_display = ('name', 'chronicles', 'reference_code',)

    def chronicles(self, obj: Organization =None):
        if obj:
            return ','.join(obj.chronicles.values_list('name', flat=True))


class ReportPrestigeInline(CSVImportInline):
    model = Prestige
    fields = ('membership', 'amount', 'notes')
    extra = 3
    min_num = 1
    upload_fields = ['membership', 'amount', 'notes']


@admin.register(PrestigeReport)
class PrestigeReport(admin.ModelAdmin):
    model = PrestigeReport
    inlines = (ReportPrestigeInline, )
    fields = ('organization', 'start', 'end', )


class ExperienceAwardInline(admin.TabularInline):
    model = Advancement
    fields = ('character', 'experience', 'beats', 'notes', )
    extra = 3
    min_num = 0


@admin.register(GameEvent)
class GameEventAdmin(admin.ModelAdmin):
    model = GameEvent
    fields = ('chronicle', 'number', 'event_date', 'title', )
    list_display = ('chronicle', 'number', 'event_date', )
    readonly_fields = ('number', )
    inlines = (ExperienceAwardInline, )

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if not obj:
            fields.remove('number')
        return fields


