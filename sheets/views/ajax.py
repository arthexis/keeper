from django.http import JsonResponse

from game_rules.models import Merit
from sheets.models import CharacterMerit, SkillSpeciality, CharacterPower

__all__ = (
    'available_merits',
    'character_merits',
    'character_specialities',
    'character_powers',
)


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


# Function view that returns specialities a character already has in a JSON format
def character_specialities(request):
    def bundle(item):
        return {'skill': item.skill, 'speciality': item.speciality}

    qs = SkillSpeciality.objects.filter(character_id=int(request.GET.get('char'))).order_by('skill')
    return JsonResponse({'items': [bundle(i) for i in qs.all()]})


# Function view that returns specialities a character already has in a JSON format
def character_powers(request):
    def bundle(item):
        return {'name': item.power.name, 'dots': item.rating}

    qs = CharacterPower.objects.filter(
        character_id=int(request.GET.get('char')),
        power__category__name=request.GET.get('category'))
    return JsonResponse({'powers': [bundle(i) for i in qs.all()]})


