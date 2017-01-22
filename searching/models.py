from django.db import models

# Create your models here.
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
		return self.team_name, self.home_ground
	
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
			('choice1', 'Sunny'),
			('choice2', 'Windy'),
			('choice3', 'Showers'),
			('choice4', 'Heavy Rain'),
			),
			default='choice1',
			)
	#The 2 possible options will be the 2 team names 
	#that have already been selected.
	#batting_first = models.CharField()

	def __str__(self):
		return self.away_team 
