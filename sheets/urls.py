from django.conf.urls import url
from sheets.views import ListCharacterView, EditCharacterView, CreateCharacterView


urlpatterns = [

    # Character list for a single user
    url(r'^character/list/$', ListCharacterView.as_view(), name='characters'),

    # Create / update character sheets
    url(r'^character/(?P<pk>[0-9]+)/edit/$', EditCharacterView.as_view(), name='edit-character'),
    url(r'^character/new/$', CreateCharacterView.as_view(), name='create-character'),

]
