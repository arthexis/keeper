from django.conf.urls import url
from sheets.views import ListCharacterView, EditCharacterView, CreateCharacterView, \
    available_merits, character_merits, character_specialities, character_powers


urlpatterns = [

    # Character list for a single user
    url(r'^character/list/$', ListCharacterView.as_view(), name='characters'),

    # Create / update character sheets
    url(r'^character/(?P<pk>[0-9]+)/edit/$', EditCharacterView.as_view(), name='edit-character'),
    url(r'^character/new/$', CreateCharacterView.as_view(), name='create-character'),

    # List of a all merits that can be used when creating characters
    url(r'^merits/all/$', available_merits, name='all-merits'),
    url(r'^merits/character/$', character_merits, name='character-merits'),

    # Lists of specialities for a character
    url(r'^specialities/character/$', character_specialities, name='character-specialities'),

    # List of character powers
    url(r'^powers/character/$', character_powers, name='character-powers'),

]
