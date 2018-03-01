from django.db import models
from game_rules.widgets import DotsInput, BoxesInput


class CountableField(models.PositiveSmallIntegerField):
    widget_class = None

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        self.options = {
            'clear': kwargs.pop('clear', True),
            'number': kwargs.pop('number', 10),
            'break_after': kwargs.pop('break_after', None),
        }
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        field = super().formfield(**kwargs)
        field.widget = self.widget_class(**self.options)
        return field


class DotsField(CountableField):
    description = 'A field that supports a number between 0 and 10 using circles'
    widget_class = DotsInput


class BoxesField(CountableField):
    description = 'A field that supports a number between 0 and 10 using boxes'
    widget_class = BoxesInput

