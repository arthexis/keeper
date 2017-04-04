from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'orgs/index.html'


__all__ = ('IndexView', )
