from django.urls import reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from sheets.models import Character
from sheets.forms import CreateCharacterForm, EditCharacterForm
from django.contrib import messages


class CharacterMixin(object):
    template_name = "sheets/character.html"
    model = Character
    context_object_name = 'character'


class CreateCharacterView(CharacterMixin, CreateView):
    form_class = CreateCharacterForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "There was an error creating the character.")
        return response

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse("sheets:edit-character", kwargs={'pk': self.object.pk})


class EditCharacterView(CharacterMixin, UpdateView):
    form_class = EditCharacterForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "There was an error saving the character.")
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        messages.success(self.request, "Your character has been updated, you can make additional changes below.")
        return reverse("sheets:edit-character", kwargs={'pk': self.object.pk})


class ListCharacterView(TemplateView):
    template_name = "sheets/character_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = Character.objects.filter(user=self.request.user)
        return context


