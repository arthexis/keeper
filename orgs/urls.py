from django.conf.urls import url
from orgs.views import *


urlpatterns = [

    # Main view for the entire application
    url(r'^$', IndexView.as_view(), name='index'),

]
