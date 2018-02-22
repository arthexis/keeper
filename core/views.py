import logging

from django.shortcuts import redirect
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

__all__ = (
    'Index',
)


# The IndexView has been declared here to keep it separate from the rest
# This is because it doesn't belong to any specific application
class Index(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)
