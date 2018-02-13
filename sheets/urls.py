from keeper.utils import path
from sheets.views import *

app_name = "sheets"
urlpatterns = [

    # Character list for a single user
    path('char/list/', ListCharacters, 'list-char'),

    # Create / update character sheets
    path('char/<int:pk>/edit/', EditCharacter, 'edit-char'),
    path('char/new/', CreateCharacter, 'create-char'),

    # List of a all merits that can be used when creating characters
    path('merit/all/', available_merits, 'all-merits'),
    path('merit/char/', character_merits, 'char-merits'),

    # Lists of specialities for a character
    path('speciality/char/', character_specialities, 'char-specialty'),

    # List of character powers
    path('power/char/', character_powers, 'char-power'),

]
