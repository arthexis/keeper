from django.contrib import admin
from orgs.models import Prestige, Membership, Event, Chronicle
# from sheets.models import Assistance


class PrestigeInline(admin.TabularInline):
    model = Prestige
    extra = 0
    fields = ('prestige_beats', 'details', 'awarded_on')
    readonly_fields = ('awarded_on',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    fields = (
        ('user', 'status'),
        ('joined_on', 'starts_on', 'ends_on'),
        ('phone',)
    )
    list_display = ('user_name', 'user_email', 'status', 'prestige_level')
    inlines = (PrestigeInline,)


class EventInline(admin.TabularInline):
    model = Event
    fields = ('name', 'event_date', 'planning_document')
    extra = 0
    show_change_link = True


@admin.register(Chronicle)
class ChronicleAdmin(admin.ModelAdmin):
    model = Chronicle
    inlines = (EventInline,)
    fields = (
        ('name', 'code'),
        ('default_template',),
        ('theme', 'mood'),
        ('venue_storyteller', 'domain_storyteller'),
        ('venue_coordinator', 'domain_coordinator'),
        ('storytelling_group', 'coordinating_group'),
    )
    list_display = ('name', 'code', 'default_template', 'venue_storyteller', 'venue_coordinator')


# class EventAssistanceInline(admin.TabularInline):
#     model = Assistance
#     fields = ('character', 'storyteller_beats', 'coordinator_beats', 'details')
#     extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('short_name', 'event_date', 'chronicle', 'name')
    # inlines = (EventAssistanceInline,)

