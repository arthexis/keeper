from django.conf import settings
from django.urls import include, path
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
                logger.error(f"User <{user}> is missing a Profile.")
                context['profile'] = None
            context['req_member_form'] = \
                RequestMembershipForm(request=self.request)
        return context


# Most URL patterns are defined using namespaces

urlpatterns = [

    # Organization and Membership namespace
    path('orgs/', include('orgs.urls', namespace='orgs')),

    # Character sheet stuff namespace
    path('sheets/', include('sheets.urls')),

    # Character sheet stuff namespace
    path('systems/', include('systems.urls')),

    # Main IndexView (homepage)
    path('', IndexView.as_view(), name='index'),

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

