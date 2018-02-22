import logging

from django.conf import settings
from django.db import OperationalError
from django.urls import include, path
from django.contrib import admin

from core.rest import router
from core.views import Index, EditMyProfile

logger = logging.getLogger(__name__)


# Most URL patterns are defined using namespaces
# https://docs.djangoproject.com/en/2.0/ref/urls/

urlpatterns = [

    # Character sheet stuff namespace
    path('sheets/', include('sheets.urls')),

    # Admin site
    # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/
    path('admin/', admin.site.urls),

    # REST Framework
    # http://www.django-rest-framework.org/
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # Django-Select2
    path('select2/', include('django_select2.urls')),

    # All Auth urls
    path('accounts/', include('allauth.urls')),

    # Edit Profile
    path('profile/', EditMyProfile.as_view(), name="profile"),

    # Main IndexView (homepage)
    path('', Index.as_view(), name='index'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


# On start setup for sites and social accounts

if settings.SITE_ID == 1:
    logger.info('Using development site configuration.')
    try:
        from django.contrib.sites.models import Site
        Site.objects.filter(pk=settings.SITE_ID).update(domain=settings.SITE_DOMAIN, name=settings.SITE_NAME)

        if settings.FACEBOOK_LOGIN_ENABLED:
            logger.info('Facebook login enabled, doing auto-setup.')
            from allauth.socialaccount.models import SocialApp
            app, created = SocialApp.objects.get_or_create(name='Facebook')
            app.client_id = settings.FACEBOOK_APP_ID
            app.secret = settings.FACEBOOK_APP_SECRET
            app.provider = 'facebook'
            app.save()
            if created:
                logger.info(f'New social app created: {app.name}')
            if not app.sites.count():
                logger.info(f'Site {settings.SITE_ID} added to social app.')
                app.sites.add(settings.SITE_ID)
    except OperationalError:
        pass




