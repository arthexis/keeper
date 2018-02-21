import logging

from django.conf import settings
from django.urls import include, path
from django.contrib import admin

import django.contrib.auth.views as auth_views

from sheets.rest import router
from orgs.views import Index

logger = logging.getLogger(__name__)


# Most URL patterns are defined using namespaces

urlpatterns = [

    # Organization and Membership namespace
    path('orgs/', include('orgs.urls')),

    # Character sheet stuff namespace
    path('sheets/', include('sheets.urls')),

    # Character sheet stuff namespace
    path('systems/', include('systems.urls')),

    # Authentication views (default with custom templates)
    # path('accounts/login/', auth_views.LoginView.as_view(template_name="index.html"), name="login"),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout"),

    # Admin
    path('admin/', admin.site.urls),

    # REST Framework
    # http://www.django-rest-framework.org/

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # Django-Select2
    path('select2/', include('django_select2.urls')),

    # All Auth urls
    path('accounts/', include('allauth.urls')),

    # Main IndexView (homepage)
    path('', Index.as_view(), name='index'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if settings.SITE_ID < 3:
    from django.contrib.sites.models import Site
    Site.objects.filter(pk=settings.SITE_ID).update(domain=settings.SITE_DOMAIN, name=settings.SITE_NAME)

