from django.contrib import admin
from orgs.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    fields = ('user', 'phone', 'information')
    list_display = ('username', 'email', 'first_name', 'last_name')


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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('name', 'event_date')

