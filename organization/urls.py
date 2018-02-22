from organization.views import *
from keeper.utils import path

app_name = 'orgs'
urlpatterns = [

    # Edit Profile details
    path('profile/', EditProfile, "profile"),

    # Forms for creating / modifying Organizations
    path('org/new/', CreateOrganization, 'create-org'),
    path('org/<int:pk>/', ViewOrganization, 'view-org'),

    # Requesting Membership
    path('member/new/', ViewMembership, "request-membership"),
    path('member/<int:pk>/cancel/', CancelMembership, "cancel-membership"),

    # Create/edit event
    path('org/<int:pk>/event/new/', CreateEvent, 'create-event'),
    path('event/<int:pk>/', ViewEvent, 'view-event'),
    path('event/<int:pk>/edit/', EditEvent, 'edit-event'),
    path('event/<int:pk>/delete/', DeleteEvent, 'delete-event'),
]
