from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^sheets/', include('sheets.urls', namespace='sheets')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

