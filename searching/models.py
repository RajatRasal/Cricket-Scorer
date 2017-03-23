"""
Django uses an ORM (Object-Relation Mapper) to create database models.
This means that each child class which inherits from models.Model parent will be
converted to a table and each attribute (variable) in it will be treated as a
field in the table. This conversion between Python code and SQLite syntax occurs
when I run the 'python3 manage.py makemigrations' in the command line. I must
then run 'python3 manage.py migrate' in order to run the SQLite commands that
have been created by the previous shell command.
"""

from datetime import datetime

from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator


class Team(models.Model):
    """ Table in the database containing a list of all the teams that
    have played games using the app. Everytime a new team is registered
    it will go into into this table in the database. """

    # Django assumes every field is non-nullable (cannot be left empty) unless
    # otherwise specified. Therefore the 'blank=True' paramter needs to be set
    # to remove this default functionality.

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

    # Team names will be a foreign key from the 'Team' table above,
    # to prevent data redundancy.
    # models.PROTECT -> prevents the deletion of any referenced objects
    # related_name -> to avoid ambiguity when accessing the Teams from the Match object

    home_team = models.ForeignKey(Team, related_name='home_team',
                                  on_delete=models.PROTECT, default=0)
    away_team = models.ForeignKey(Team, related_name='away_team',
                                  on_delete=models.PROTECT, default=0)
    date = models.DateField()

    # Ground location will take the value from the 'home_ground' fields
    # in the 'Team' table of the teams that have
    # been selected in the 'Team' table and makes these the only
    # possible options for selection.
    ground_location = models.CharField(
        max_length=50,
        choices=(('home', 'home'), ('away', 'away')),
        default='home')
    # blank = True => means the field is not required when used in a form
    # null = True => means the field can be left null in the DB
    umpire_1 = models.CharField(max_length=50, blank=True, null=True)
    umpire_2 = models.CharField(max_length=50, blank=True, null=True)
    weather = models.CharField(max_length=30,
                               choices=(
                                   ('1', 'sunny'),
                                   ('2', 'sunny spells'),
                                   ('3', 'windy'),
                                   ('4', 'showers'),
                                   ('5', 'heavy rain'),
                                   ('6', 'rain and sun'),
                                   ('7', 'cloudy'),
                                   ('8', 'overcast'),
                                   ('9', 'other'),),
                               default='0')
    batting_first = models.CharField(
        max_length=50,
        choices=(('home', 'home'), ('away', 'away')),
        default='home')
    overs = models.IntegerField(default=1)
    # The results will be set as a string once we have finished scoring a game.
    result = models.CharField(max_length=50, blank=True, null=True)
    # result = models.CharField(max_length=50, default='x')

    def __str__(self):
        return str(self.home_team) + ' vs ' + str(self.away_team)


class Player(models.Model):
    """
    Table in the database containing the details of each player
    which will have compiled statistics how each player has
    performed in the matches they have played. Also includes
    the data about which club a player is playing for and their name
    """

    # field in the table which have stored player metadata
    player_name = models.CharField(max_length=50, default='NO NAME GIVEN')
    current_team_name = models.ForeignKey(Team, on_delete=models.PROTECT, default=0)
    matches_played = models.PositiveIntegerField(null=True, blank=True)

    # fields which store compiled batting match statistics
    # these will be compiled by a views.py function
    batting_total_runs_scored = models.PositiveIntegerField(null=True, blank=True)
    batting_inning = models.PositiveIntegerField(null=True, blank=True)
    batting_high_score = models.PositiveIntegerField(null=True, blank=True)
    batting_average = models.FloatField(null=True, blank=True)
    batting_strike_rate = models.FloatField(null=True, blank=True)
    batting_50s = models.PositiveIntegerField(null=True, blank=True)
    batting_100s = models.PositiveIntegerField(null=True, blank=True)

    # fields which store compiled bowling match statistics
    # these will be compiled by a views.py function
    bowling_total_balls_faced = models.PositiveIntegerField(null=True, blank=True)
    bowling_runs_conceded = models.PositiveIntegerField(null=True, blank=True)
    bowling_wickets = models.PositiveIntegerField(null=True, blank=True)
    bowling_best_figures = models.CharField(max_length=10, default='NA')
    bowling_average = models.FloatField(null=True, blank=True)
    bowling_strike_rate = models.FloatField(null=True, blank=True)
    bowling_economy = models.FloatField(null=True, blank=True)
    bowling_5ws = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.player_name


class MatchTeamPlayer(models.Model):
    """
    Table will be used to link the Match, Team and Player entities. This will
    allow for there to be a one-to-many relationship between each of these
    entities. Should also make it easier to query data when producing stats
    """

    player_id = models.ForeignKey(Player, on_delete=models.PROTECT)
    team_id = models.ForeignKey(Team, on_delete=models.PROTECT)
    match_id = models.ForeignKey(Match, on_delete=models.PROTECT)
    date = models.DateField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return str(self.player_id)
