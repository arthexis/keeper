from django.db import models
from systems.widgets import *


class DotsField(models.PositiveSmallIntegerField):
    description = 'A field that supports a number between 0 and 10'

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        self.clear = kwargs.pop('clear', True)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        field = super().formfield(**kwargs)
        field.widget = DotsInput(circles=10, clear=self.clear)
        return field

