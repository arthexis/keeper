from django.db import models
from systems.widgets import DotsInput


class DotsField(models.PositiveSmallIntegerField):
    description = 'A field that supports a number between 0 and 10'

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        self.clear = kwargs.pop('clear', True)
        self.circles = kwargs.pop('circles', 10)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        field = super().formfield(**kwargs)
        field.widget = DotsInput(circles=self.circles, clear=self.clear)
        return field


class BookReferenceField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)



