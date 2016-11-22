from django.db import models

from systems.consts import *


class DotsField(models.PositiveSmallIntegerField):

    description = 'A field that supports a number between 0 and 10'

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = TEN_DOTS
        kwargs['default'] = 0
        super().__init__(*args, **kwargs)