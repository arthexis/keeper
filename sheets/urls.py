from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.SimpleRouter()
router.register('characters', CharacterViewSet)

app_name = "sheets"
urlpatterns = [

    path('', include(router.urls)),

]
