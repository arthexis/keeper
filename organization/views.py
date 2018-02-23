from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import RedirectView

from core.models import UserProfile
from .models import Invitation


class AcceptInvite(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        code = kwargs['code']
        invitation = get_object_or_404(Invitation, code=code)
        invitation.is_accepted = True
        invitation.save()
        user = UserProfile.objects.filter(email=invitation.email_address)

        if user.exists():
            invitation.redeem(user)
            if self.request.user == user:
                return reverse('index')
            return reverse('account_login')

        session = self.request.session
        session['chapter'] = invitation.chapter.name
        session['invite_code'] = invitation.code
        session['invite_email'] = invitation.email_address
        return reverse('account_signup')
