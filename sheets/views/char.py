import json

from django.urls import reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib import messages
from django.shortcuts import get_object_or_404

from systems.models import Merit, Power
from sheets.models import Character, CharacterMerit, SkillSpeciality, CharacterPower
from sheets.forms import CreateCharacterForm, EditCharacterForm


__all__ = (
    'CreateCharacter',
    'EditCharacter',
    'ListCharacters',
)


class _CharacterMixin(object):
    template_name = "sheets/character.html"
    model = Character
    context_object_name = 'character'


class CreateCharacter(_CharacterMixin, CreateView):
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
        return reverse("sheets:edit-char", kwargs={'pk': self.object.pk})


class EditCharacter(_CharacterMixin, UpdateView):
    form_class = EditCharacterForm

    def get_template_names(self):
        if self.object and self.object.template:
            return [
                f'sheets/custom/{self.object.template.name}.html',
                'sheets/character.html']
        return super().get_template_names()

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "There was an error saving the character.")
        return response

    def form_valid(self, form):
        response = super().form_valid(form)

        # Save merit data independently
        merit_data = form.cleaned_data.get('merits', None)
        if merit_data:
            CharacterMerit.objects.filter(character=form.instance).delete()
            for merit_pk, dots in json.loads(merit_data).items():
                if merit_pk == 'null' or dots == 'null':
                    # This happens when the user leaves merits blank
                    continue
                merit_pk, dots = int(merit_pk), int(dots)
                if dots < 1:
                    continue
                CharacterMerit.objects.create(
                    character=form.instance, rating=dots,
                    merit=get_object_or_404(Merit, pk=merit_pk))

        # Save speciality data independently
        speciality_data = form.cleaned_data.get('specialities', None)
        if speciality_data:
            SkillSpeciality.objects.filter(character=form.instance).delete()
            for skill, speciality in json.loads(speciality_data).items():
                if skill == 'null' or speciality == 'null' or speciality == '':
                    # This happens when the user leaves merits blank
                    continue
                SkillSpeciality.objects.create(
                    character=form.instance, speciality=speciality, skill=skill)

        # Save power data independently
        power_data = form.cleaned_data.get('powers', None)
        if power_data:
            CharacterPower.objects.filter(character=form.instance).delete()
            for power_name, dots in json.loads(power_data).items():
                power = get_object_or_404(Power, name=power_name)
                CharacterPower.objects.create(character=form.instance, power=power, rating=dots)

        return response

    def get_success_url(self):
        messages.success(self.request, "Your character has been updated, you can make additional changes below.")
        return reverse("sheets:edit-char", kwargs={'pk': self.object.pk})


class ListCharacters(TemplateView):
    template_name = "sheets/character_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = Character.objects.filter(user=self.request.user)
        return context
