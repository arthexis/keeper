from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from sheets.models import Character


class CreateCharacterView(LoginRequiredMixin, CreateView):
    template_name = "sheets/character.html"
    model = Character
    fields = ('name', 'template')


class UpdateCharacterView(LoginRequiredMixin, UpdateView):
    template_name = "sheets/character.html"
    model = Character
    fields = ('name', 'template')


class ListCharacterView(LoginRequiredMixin, ListView):
    template_name = "sheets/character_list.html"
    model = Character

