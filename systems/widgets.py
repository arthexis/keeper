from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class DotsInput(Widget):
    input_type = None

    def __init__(self, clear=True, circles=5):
        super().__init__()
        self.clear = clear
        self.circles = circles

    def render(self, name, value, attrs=None):
        dots = ""
        for i in range(1, self.circles + 1):
            dots += format_html('<input type="radio" value="{}"></input>', i)
        if self.clear:
            dots += format_html('<button class="clear">x</button>')
        return format_html(
            '<div class="dots"><input type="hidden" name="{}" value={}>{}</div>',
            name, value, mark_safe(dots))

    class Media:
        css = {'all': ('css/dots.css', )}
        js = ('js/dots.js', )

