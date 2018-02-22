from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import HttpResponseRedirect
from django_object_actions import BaseDjangoObjectActions
from allauth.socialaccount.models import EmailAddress, SocialApp, SocialAccount, SocialToken


__all__ = (
    'HiddenAdmin',
    'SimpleActionsModel',
    'SaveRedirectAdmin',
)


class HiddenAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SimpleActionsModel(BaseDjangoObjectActions, admin.ModelAdmin):

    def __init__(self, model, admin_site):
        actions = list(self.change_actions)
        for action in actions:
            if not hasattr(self, action):

                def inner(self, obj):
                    func = getattr(obj, action, None)
                    if callable(func):
                        return func(user=self.user)

                inner.label = action.replace('_', ' ')
                setattr(self, action, inner)

        super().__init__(model, admin_site)

    def get_change_actions(self, request, object_id, form_url):
        if not object_id:
            return []
        actions = list(super().get_change_actions(request, object_id, form_url))
        obj = self.model.objects.get(pk=object_id)
        user = request.user
        for action in actions:
            func = getattr(obj, f'can_{action}', None)
            if func and not func(user=user):
                actions.remove(action)
        return actions


class SaveRedirectAdmin(admin.ModelAdmin):

    def get_save_redirect_url(self, request, obj):
        return ''

    def response_add(self, request, obj, post_url_continue=None):
        if '_continue' not in request.POST:
            url = self.get_save_redirect_url(request, obj)
            if url:
                return HttpResponseRedirect(url)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            url = self.get_save_redirect_url(request, obj)
            if url:
                return HttpResponseRedirect(url)
        return super().response_change(request, obj)


# Unregistered unnecessary admin modules

if not settings.SHOW_HIDDEN_ADMIN_MODULES:
    admin.site.unregister(EmailAddress)
    admin.site.unregister(Group)
    admin.site.unregister(SocialApp)
    admin.site.unregister(SocialAccount)
    admin.site.unregister(SocialToken)
    admin.site.unregister(Site)


