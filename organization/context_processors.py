from .models import Membership


def membership(request):
    context = {}
    if request.user:
        try:
            member_pk = request.session['membership']
            context['membership'] = Membership.objects.get(pk=member_pk, user=request.user)
        except (KeyError, Membership.DoesNotExist):
            context['membership'] = obj = Membership.objects.filter(user=request.user).first()
            if obj:
                request.session['membership'] = obj.pk
    return context

