"""
Django uses an ORM (Object-Relation Mapper) to create database models.
This means that each child class which inherits from models.Model parent will be
converted to a table and each attribute (variable) in it will be treated as a
field in the table. This conversion between Python code and SQLite syntax occurs
when I run the 'python3 manage.py makemigrations' in the command line. I must
then run 'python3 manage.py migrate' in order to run the SQLite commands that
have been created by the previous shell command.

Contains the ball-by-ball table
"""

from django.db import models

from searching.models import Match


class BallByBall(models.Model):
    """
    BallByBall table will be used store details about the event of each ball
    
    Each of the private properties below is a column/attribute in the table.
    
    The purpose of each column names is pretty self-explanantory. 
    """

    # Will store the match id of the latest game
    match_id = models.ForeignKey(Match, related_name='match_id',
                                 on_delete=models.PROTECT)
    onstrike = models.CharField(max_length=30, blank=True, null=True)
    offstrike = models.CharField(max_length=30, blank=True, null=True)
    bowler = models.CharField(max_length=30, blank=True, null=True)
    over = models.IntegerField(default=0, blank=True, null=True)
    ball_in_over = models.IntegerField(default=0, blank=True, null=True)
    total_runs = models.IntegerField(default=0, blank=True, null=True)
    total_wickets = models.IntegerField(default=0, blank=True, null=True)
    how_out = models.CharField(max_length=20, blank=True, null=True)
    people_involved = models.CharField(max_length=30, blank=True, null=True)
    runs = models.IntegerField(default=0, blank=True, null=True)
    extras = models.IntegerField(default=0, blank=True, null=True)
    extras_type = models.CharField(max_length=20, blank=True, null=True)
    innings = models.IntegerField(default=1)

    def __str__(self):
        """
        When a 'BallByBall' record/object is referred to in the Django admin view 
        (according to searching/admin.py file) , we cannot display everything in the 
        record. The value returned by this function will be the value seen. So in 
        this case, to represent a 'Team' instance, you will see the value stored in the 
        'team_name' field for that record.
        """
        return 'Match: {}, Ball: {}.{}'.format(self.match_id,
                                               self.over,
                                               self.ball_in_over)
