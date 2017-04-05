from django.conf.urls import url
from orgs.views import *


urlpatterns = [

    # Main view for the entire application
    url(r'^$', IndexView.as_view(), name='index'),

    # Registration for new Members
    url(r'^register/', RegistrationView.as_view(), name='register'),

    # Membership details
    url(r'^profile/(?P<pk>[0-9]+)/', ProfileDetailView.as_view(), name="profile"),

    # Pending Email Verification Screen
    url(r'^pending/', PendingView.as_view(), name='pending'),

    # Login for regular users
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),

]
