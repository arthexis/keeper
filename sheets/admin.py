from django.contrib import admin
from sheets.models import *

# Register your models here.

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    model = Character
    fieldsets = (
        (None, {
            'fields': ('name', 'template'),
        }),
        ('Attributes', {
            'fields': (
                ('intelligence', 'strength', 'presence'),
                ('wits', 'dexterity', 'manipulation'),
                ('resolve', 'stamina', 'composure'),
            ),
        }),
        ('Skills', {
            'fields': (
                ('academics', 'athletics', 'animal_ken'),
                ('computer', 'brawl', 'empathy'),
                ('crafts', 'drive', 'expression'),
                ('investigation', 'firearms', 'intimidation'),
                ('medicine', 'larceny', 'persuasion'),
                ('occult', 'stealth', 'socialize'),
                ('politics', 'survival', 'streetwise'),
                ('science', 'weaponry', 'subterfuge'),
            ),
        }),
    )

    list_display = ('name', 'template',)

