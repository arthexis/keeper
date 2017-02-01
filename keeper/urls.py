from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from views import CreateCharacterView, UpdateCharacterView, ListCharacterView

urlpatterns = [

    # Users Site
    url(r'^character/create/', CreateCharacterView.as_view(), name="character_create"),
    url(r'^character/update/(?P<pk>[0-9]+)/', UpdateCharacterView.as_view(), name="character_update"),
    url(r'^$', ListCharacterView.as_view(), name="character_list"),

    # Authentication
    url('^', include('django.contrib.auth.urls')),

    # Admin
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

