from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [

    # Organization and Membership namespace
    url(r'^o/', include('orgs.urls', namespace='orgs')),

    # Redirect main page to orgs:index
    url(r'^$', RedirectView.as_view(url=reverse_lazy('orgs:index')), name='index'),

    # Authentication
    url('^', include('django.contrib.auth.urls')),

    # Admin
    url(r'^a/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Django-Select2
    url(r'^select2/', include('django_select2.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

