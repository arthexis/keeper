from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class CountableInput(Widget):
    """ Represents a field with dots useful for skills and attributes.

    kwargs: number, break_after, type_attr
    """
    type_attr = None

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    def render(self, name, value, attrs=None, renderer=None):
        html = ""
        insert_break = False
        type_attr = self.type_attr
        number = self.kwargs['number']
        break_after = self.kwargs['break_after']
        for i in range(1, number + 1):
            if insert_break:
                html += '<br>'
                insert_break = False
            html += format_html('<input type="{}" value="{}"></input>', type_attr,  i)
            if break_after is not None and i % break_after == 0:
                insert_break = True
        if self.kwargs['clear']:
            html += format_html('<button class="clear">x</button>')
        return format_html(
            '<div class="dots"><input type="hidden" name="{}" value={}>{}</div>',
            name, value, mark_safe(html))

    class Media:
        css = {'all': ('css/dots.css', )}
        js = ('admin/js/inlines.js', 'js/dots.js', )


class DotsInput(CountableInput):
    type_attr = 'radio'


class BoxesInput(CountableInput):
    type_attr = 'checkbox'

