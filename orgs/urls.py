from django.conf.urls import url
from orgs.views import *


urlpatterns = [

    # Main view for the entire application
    url(r'^$', IndexView.as_view(), name='index'),

    # Registration for new Members
    url(r'^register/', RegistrationView.as_view(), name='register'),

    # Edit Profile details
    url(r'^profile/$', RedirectMyProfileView.as_view(), name="profile"),
    url(r'^profile/(?P<pk>[0-9]+)/', EditProfileView.as_view(), name="profile"),

    # Pending Email Verification Screen
    url(r'^pending/', PendingView.as_view(), name='pending'),
    url(r'^verification/(?P<pk>[0-9]+)/(?P<code>[a-zA-Z]+)/', VerificationView.as_view(), name='verification'),
    url(r'^recovery/$', RequestPasswordRecoveryView.as_view(), name='recovery'),

    # Login for regular users
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),

    # Forms for creating / modifying Organizations
    url(r'^organization/$', CreateOrganizationView.as_view(), name='organization'),
    url(r'^organization/(?P<pk>[0-9]+)/', DetailOrganizationView.as_view(), name='organization'),
    url(r'^organization/edit/(?P<pk>[0-9]+)/', EditOrganizationView.as_view(), name='edit-organization'),

    # Requesting Membership
    url(r'^membership/$', MembershipView.as_view(), name="membership"),
    url(r'^membership/cancel/(?P<pk>[0-9]+)$', CancelMembershipView.as_view(), name="cancel-membership"),

]
