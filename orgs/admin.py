from django.contrib import admin
from orgs.models import *
# from sheets.models import Assistance


# class PrestigeInline(admin.TabularInline):
#     model = Prestige
#     extra = 0
#     fields = ('prestige_beats', 'details', 'awarded_on')
#     readonly_fields = ('awarded_on',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    fields = (
        ('user', ),
    )
    list_display = ('user', )


# class EventInline(admin.TabularInline):
#     model = Event
#     fields = ('name', 'event_date', 'planning_document')
#     extra = 0
#     show_change_link = True
#
#
# @admin.register(Chronicle)
# class ChronicleAdmin(admin.ModelAdmin):
#     model = Chronicle
#     inlines = (EventInline,)
#     fields = (
#         ('name', 'code'),
#         ('default_template',),
#         ('theme', 'mood'),
#         ('venue_storyteller', 'domain_storyteller'),
#         ('venue_coordinator', 'domain_coordinator'),
#         ('storytelling_group', 'coordinating_group'),
#     )
#     list_display = ('name', 'code', 'default_template', 'venue_storyteller', 'venue_coordinator')
#
#
# # class EventAssistanceInline(admin.TabularInline):
# #     model = Assistance
# #     fields = ('character', 'storyteller_beats', 'coordinator_beats', 'details')
# #     extra = 0
#
#
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     model = Event
#     list_display = ('short_name', 'event_date', 'chronicle', 'name')
#     # inlines = (EventAssistanceInline,)

