from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView

from orgs.models import Profile
from orgs.forms import RequestMembershipForm
from sheets.rest import router

import logging
logger = logging.getLogger(__name__)


# The IndexView has been declared here to keep it separate from the rest
# This is because it doesn't belong to any specific application
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            context['form'] = AuthenticationForm()
        else:
            try:
                context['profile'] = profile = Profile.objects.get(user=user)
                upcoming_events = profile.upcoming_events()
                context['upcoming_events'] = upcoming_events[:5]
                context['remaining_events'] = upcoming_events.count() - 5
            except Profile.DoesNotExist:
                logger.error(f"User <{user}> is missing a Profile object.")
                context['profile'] = None
            context['req_member_form'] = RequestMembershipForm(request=self.request)
        return context


# Most URL patterns are defined using namespaces

urlpatterns = [

    # Organization and Membership namespace
    url(r'^o/', include('orgs.urls', namespace='orgs')),

    # Character sheet stuff namespace
    url(r'^s/', include('sheets.urls', namespace='sheets')),

    # Character sheet stuff namespace
    url(r'^y/', include('systems.urls', namespace='systems')),

    # Main IndexView (homepage)
    url(r'^$', IndexView.as_view(), name='index'),

    # Authentication
    url('^', include('django.contrib.auth.urls')),

    # Admin
    url(r'^a/', admin.site.urls),

    # REST Framework
    # http://www.django-rest-framework.org/

    url(r'^r/', include(router.urls, namespace='rest')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    # Django-Select2
    url(r'^select2/', include('django_select2.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

