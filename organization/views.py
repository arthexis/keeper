from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from .models import Invitation


class AcceptInvite(RedirectView):
    url = reverse_lazy('account_signup')

    def get_redirect_url(self, *args, **kwargs):
        code = kwargs['code']
        invitation = get_object_or_404(Invitation, code=code)
        self.request.session['chapter'] = invitation.chapter.name
        self.request.session['invite_code'] = invitation.code
        self.request.session['invite_email'] = invitation.email_address
        invitation.is_accepted = True
        invitation.save()
        return super().get_redirect_url(*args, **kwargs)
