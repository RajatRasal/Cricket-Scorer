"""
This file allows the different attributes that have been configured to be
shown in the Django admininstation page which, as you can see in the
cricketscoring/urls.py file, can be accessed at with the URL "localhost/admin"
"""

from django.contrib import admin
from .models import Team, Match, Player, MatchTeamPlayer

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(MatchTeamPlayer)
