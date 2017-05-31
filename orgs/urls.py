from django.conf.urls import url
from orgs.views import *
from django.views.generic import TemplateView


urlpatterns = [

    # Registration for new Members
    url(r'^register/$', RegistrationView.as_view(), name='register'),

    # Edit Profile details
    url(r'^profile/$', RedirectMyProfileView.as_view(), name="profile"),
    url(r'^profile/(?P<pk>[0-9]+)/edit/$', EditProfileView.as_view(), name="edit-profile"),

    # Pending Email Verification Screen
    url(r'^verify/pending/$', TemplateView.as_view(template_name='orgs/pending.html'), name='pending'),
    url(r'^verify/(?P<pk>[0-9]+)/(?P<code>[a-zA-Z]+)/$', VerificationView.as_view(), name='verification'),
    url(r'^recover/$', RequestPasswordRecoveryView.as_view(), name='recovery'),

    # Login for regular users
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # Forms for creating / modifying Organizations
    url(r'^org/new/$', CreateOrganizationView.as_view(), name='create-organization'),
    url(r'^org/(?P<pk>[0-9]+)/$', DetailOrganizationView.as_view(), name='view-organization'),
    url(r'^org/(?P<pk>[0-9]+)/edit/$', EditOrganizationView.as_view(), name='edit-organization'),

    # Requesting Membership
    url(r'^member/new/$', MembershipView.as_view(), name="request-membership"),
    url(r'^member/(?P<pk>[0-9]+)/cancel/$', CancelMembershipView.as_view(), name="cancel-membership"),

    # Create/edit event
    url(r'^org/(?P<org_pk>[0-9]+)/event/new/$', CreateEventView.as_view(), name='create-event'),
    url(r'^event/(?P<pk>[0-9]+)/$', DetailEventView.as_view(), name='view-event'),
    url(r'^event/(?P<pk>[0-9]+)/edit/$', EditEventView.as_view(), name='edit-event'),
    url(r'^event/(?P<pk>[0-9]+)/delete/$', DeleteEventView.as_view(), name='delete-event'),

    # User's Upcoming Event Calendar
    url(r'^calendar/$', MyCalendarView.as_view(), name='calendar'),

]
