from django.contrib import admin
from django.http import HttpResponseRedirect
from django_object_actions import BaseDjangoObjectActions


__all__ = (
    'SimpleActionsModel',
    'SaveRedirectAdmin',
)


class SimpleActionsModel(BaseDjangoObjectActions, admin.ModelAdmin):

    def __init__(self, model, admin_site):
        actions = list(self.change_actions)
        for action in actions:
            if not hasattr(self, action):

                def inner(self, obj):
                    func = getattr(obj, action, None)
                    if callable(func):
                        return func(user=self.user)

                inner.label = action.replace('_', ' ').upper()
                setattr(self, action, inner)

        super().__init__(model, admin_site)

    def get_change_actions(self, request, object_id, form_url):
        if not object_id:
            return []
        actions = list(super().get_change_actions(request, object_id, form_url))
        obj = self.model.objects.get(pk=object_id)
        if not hasattr(obj, 'can_take_action'):
            return actions
        user = request.user
        return [a for a in actions if obj.can_take_action(a, user=user)]


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

