import json
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from sheets.models import Character, CharacterMerit
from sheets.forms import CreateCharacterForm, EditCharacterForm
from django.contrib import messages
from django.http import JsonResponse
from systems.models import Merit
from django.shortcuts import get_object_or_404


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


# Simple function view that returns merits in a JSON format
def available_merits(request):
    def pair(item):
        return {'id': item['pk'], 'text': item['name']}

    qs = Merit.objects.filter(name__icontains=request.GET.get('term', ''))
    return JsonResponse({'items': [pair(i) for i in qs.values('pk', 'name')]})


# Function view that returns merits a character already has in a JSON format
def character_merits(request):
    def bundle(item):
        return {'pk': item['merit__pk'], "text": item['merit__name'], 'dots': item['rating']}

    qs = CharacterMerit.objects.filter(character_id=int(request.GET.get('char'))).order_by('merit__name')
    return JsonResponse({'items': [bundle(i) for i in qs.values('merit__pk', 'rating', 'merit__name')]})
