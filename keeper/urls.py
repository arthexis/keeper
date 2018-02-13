import logging

from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from sheets.rest import router

from .views import Index

logger = logging.getLogger(__name__)


# Most URL patterns are defined using namespaces

urlpatterns = [

    # Organization and Membership namespace
    path('orgs/', include('orgs.urls')),

    # Character sheet stuff namespace
    path('sheets/', include('sheets.urls')),

    # Character sheet stuff namespace
    path('systems/', include('systems.urls')),

    # Main IndexView (homepage)
    path('', Index.as_view(), name='index'),

    # Authentication
    path('auth/', include('django.contrib.auth.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # REST Framework
    # http://www.django-rest-framework.org/

    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # Django-Select2
    path('select2/', include('django_select2.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

