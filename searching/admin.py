"""
This file is being used to make different data models/tables in the database 
visible from the admin view in Django. From the admin page, data can be easily
entered into the database as opposed to having to use queries to enter data 
into it. This will be useful when it comes to setting up teams and players to
go into those teams. 

From the cricket_scoring/urls.py file, you can see that the Django admin view 
can be accessed when you enter "http://localhost:PORT/admin" into the address 
bar.
"""

# Importing the Django method which allows certain tables to be displayed in
# admin settings page.
from django.contrib import admin 

# Importing the classes for the data models that we want to be able to access
# in the Django admin view. We are only importing and setting the classes 
# from the tables which are being used in the searching part of the application. 
from .models import Team, Match, Player, MatchTeamPlayer

# Setting each model such that it can be accessed in the Django admin view.
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(MatchTeamPlayer)
