from orgs.views import *
from keeper.utils import path

# noinspection PyUnresolvedReferences
import orgs.signals


app_name = 'orgs'
urlpatterns = [

    # Registration for new Members
    path('register/', Registration, 'register'),
    path('pending-verify/', PendingVerify, 'pending-verify'),

    # Edit Profile details
    path('profile/', RedirectMyProfile, "profile"),
    path('profile/<int:pk>/edit/', EditProfile, "edit-profile"),

    # Forms for creating / modifying Organizations
    path('org/new/', CreateOrganization, 'create-org'),
    path('org/<int:pk>/', ViewOrganization, 'view-org'),

    # Requesting Membership
    path('member/new/', ViewMembership, "request-membership"),
    path('member/<int:pk>/cancel/', CancelMembership, "cancel-membership"),

    # Recovering lost passwords
    path('member/recovery/', RequestPasswordRecovery, 'recovery'),

    # Create/edit event
    path('org/<int:pk>/event/new/', CreateEvent, 'create-event'),
    path('event/<int:pk>/', ViewEvent, 'view-event'),
    path('event/<int:pk>/edit/', EditEvent, 'edit-event'),
    path('event/<int:pk>/delete/', DeleteEvent, 'delete-event'),

    # User's Upcoming Event Calendar
    path('calendar/', MyCalendar, 'calendar'),

]
