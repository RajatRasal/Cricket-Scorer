"""
Django uses an ORM (Object-Relation Mapper) to create database models. This means that 
that each child class which inherits from models.Model parent will be converted to a table
and each attribute (variable) in it will be treated as a field in the table. This conversion
between Python code and SQLite syntax occurs when I run the 'python3 manage.py makemigrations'
in the command line. I must then run 'python3 manage.py migrate' in order to run the 
SQLite commands that have been created by the previous shell command. 
"""

from django.db import models

class Team(models.Model):
	"""
	Table in the database containing a list of all the teams that 
	have played games using the app. Everytime a new team is registered 
	it will go into into this table in the database
	"""

	#Django assumes every field is non-nullable (cannot be left empty) unless
	#otherwise specified. Therefore the 'blank=True' paramter needs to be set
	#to remove this default functionality. 
	team_name = models.CharField(max_length=50, blank=True)
	home_ground = models.CharField(max_length=50, blank=True)

	def __str__(self):
                """
                When a 'Team' record/object is referred to in the Django admin view, we
                cannot display everything in the record. The value returned by this 
                function will be the value seen. So in this case, to represent a 'Team' 
                instance, you will see the value stored in the 'team_name' field for 
                that record. 
                """
                return self.team_name
	
class Match(models.Model):
	"""
	Table in the database containing the details of each match 
	that is played. It will not include details about the scores 
	and players in each team, but more admin-style info, i.e. 
	where the ground is, number of overs being played, teams names,
	umpire names etc.
	"""

	#Team names will be a foreign key from the 'Team' table above, 
	#to prevent data redundancy.
	#models.PROTECT -> prevents the deletion of any referenced objects  
	#related_name -> to avoid ambiguity when accessing the Teams from the Match object 
	home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.PROTECT, default=0)
	away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.PROTECT, default=0)
	date = models.DateField()
	#Ground location will take the value from the 'home_ground' fields 
	#in the 'Team' table of the teams that have 
	#been selected in the 'Team' table and makes these the only 
	#possible options for selection.
	ground_location = models.CharField(max_length=50)
	umpire_1 = models.CharField(max_length=50)
	umpire_2 = models.CharField(max_length=50)
	weather = models.CharField(
			max_length=30,
			choices = (
			('0', ' '),
			('1', 'sunny'),
			('2', 'sunny spells'),
			('3', 'windy'),
			('4', 'showers'),
			('5', 'heavy rain'),
			('6', 'rain and sun'),
			('7', 'cloudy'),
			('8', 'overcast'),
			('9', 'other'),
			),
			default='0',
			)
	#The 2 possible options will be the 2 team names 
	#that have already been selected.
	#batting_first = models.CharField()

	def __str__(self):
		return self.away_team 
